from __future__ import annotations

import json
import os
import shutil
import time
import uuid
from pathlib import Path

import numpy as np
import pandas as pd
from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from autospectra.config import (
    ALLOWED_EXTENSIONS,
    CLASS_NAMES,
    MAX_UPLOAD_MB,
    MAX_WINDOWS,
    RESULT_DIR,
    UPLOAD_DIR,
)
from autospectra.modeling import ModelRegistry
from autospectra.plotting import (
    confidence_timeline,
    message_rate_timeline,
    prediction_distribution,
    probability_heatmap,
)
from autospectra.preprocessing import process_can_file
from autospectra.reporting import generate_incident_record, summarise_predictions


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY", "autospectra-development-key"),
        MAX_CONTENT_LENGTH=MAX_UPLOAD_MB * 1024 * 1024,
        JSON_SORT_KEYS=False,
    )

    registry = ModelRegistry()
    app.extensions["autospectra_registry"] = registry

    def allowed_file(filename: str) -> bool:
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    def model_name(model_key: str) -> str:
        return registry.DISPLAY_NAMES.get(model_key, model_key)

    @app.context_processor
    def inject_globals():
        return {
            "project_name": "AutoSPECTRA",
            "class_names": CLASS_NAMES,
            "registry_status": registry.status(),
        }

    @app.get("/")
    def index():
        return render_template(
            "index.html",
            available_models=registry.available_models,
            default_model=registry.default_model_key,
            max_upload_mb=MAX_UPLOAD_MB,
            max_windows=MAX_WINDOWS,
        )

    @app.get("/about")
    def about():
        return render_template("about.html")

    @app.get("/health")
    def health():
        status = registry.status()
        return jsonify(
            {
                "status": "ok" if status["available_models"] else "degraded",
                "project": "AutoSPECTRA",
                **status,
            }
        )

    @app.post("/analyze")
    def analyze():
        if not registry.available_models:
            return render_template(
                "error.html",
                title="No trained model found",
                message=(
                    "Copy the trained AutoSPECTRA model artifacts into the app's models/ "
                    "folder or set AUTOSPECTRA_MODEL_DIR."
                ),
            ), 503

        uploaded = request.files.get("can_file")
        if uploaded is None or uploaded.filename == "":
            return render_template(
                "error.html",
                title="No CAN file selected",
                message="Choose a .csv, .txt, or .log CAN capture before starting analysis.",
            ), 400

        if not allowed_file(uploaded.filename):
            return render_template(
                "error.html",
                title="Unsupported file type",
                message="Supported extensions are .csv, .txt, and .log.",
            ), 400

        model_key = request.form.get("model_key", registry.default_model_key or "")
        available_keys = {item["key"] for item in registry.available_models}
        if model_key not in available_keys:
            return render_template(
                "error.html",
                title="Model unavailable",
                message="Select one of the trained models shown on the dashboard.",
            ), 400

        try:
            stride = int(request.form.get("stride", registry.expected_window_size))
            max_windows = int(request.form.get("max_windows", MAX_WINDOWS))
        except ValueError:
            return render_template(
                "error.html",
                title="Invalid analysis settings",
                message="Stride and maximum windows must be whole numbers.",
            ), 400

        stride = max(1, min(stride, registry.expected_window_size * 4))
        max_windows = max(1, min(max_windows, MAX_WINDOWS))

        run_id = uuid.uuid4().hex
        run_upload_dir = UPLOAD_DIR / run_id
        run_result_dir = RESULT_DIR / run_id
        run_upload_dir.mkdir(parents=True, exist_ok=True)
        run_result_dir.mkdir(parents=True, exist_ok=True)

        filename = secure_filename(uploaded.filename)
        upload_path = run_upload_dir / filename
        uploaded.save(upload_path)

        started = time.perf_counter()
        try:
            batch = process_can_file(
                upload_path,
                window_size=registry.expected_window_size,
                stride=stride,
                max_windows=max_windows,
            )
            probabilities = registry.predict(model_key, batch.features, batch.sequences)
        except Exception as exc:
            shutil.rmtree(run_upload_dir, ignore_errors=True)
            shutil.rmtree(run_result_dir, ignore_errors=True)
            return render_template(
                "error.html",
                title="Analysis failed",
                message=str(exc),
            ), 500

        elapsed_seconds = time.perf_counter() - started
        predictions = probabilities.argmax(axis=1)
        confidences = probabilities.max(axis=1)

        result_frame = batch.metadata.copy()
        result_frame["predicted_index"] = predictions
        result_frame["predicted_class"] = [CLASS_NAMES[index] for index in predictions]
        result_frame["confidence"] = confidences
        for class_index, class_name in enumerate(CLASS_NAMES):
            result_frame[f"probability_{class_name.lower()}"] = probabilities[:, class_index]

        model_display_name = model_name(model_key)
        records = []
        narratives = []
        for index in range(len(result_frame)):
            record, narrative = generate_incident_record(
                probabilities[index],
                result_frame.iloc[index],
                model_display_name,
                registry.expected_window_size,
            )
            records.append(record)
            narratives.append(narrative)
        result_frame["incident_narrative"] = narratives

        summary = summarise_predictions(probabilities)
        summary.update(
            {
                "model_key": model_key,
                "model_name": model_display_name,
                "filename": filename,
                "window_size": registry.expected_window_size,
                "stride": stride,
                "valid_frames_read": batch.total_valid_frames,
                "invalid_lines_skipped": batch.invalid_lines,
                "truncated_at_limit": batch.truncated,
                "processing_seconds": elapsed_seconds,
                "windows_per_second": len(result_frame) / max(elapsed_seconds, 1e-9),
            }
        )

        csv_name = "autospectra_window_predictions.csv"
        json_name = "autospectra_incident_report.json"
        summary_name = "autospectra_summary.json"
        result_frame.to_csv(run_result_dir / csv_name, index=False)
        (run_result_dir / json_name).write_text(
            json.dumps(records, indent=2), encoding="utf-8"
        )
        (run_result_dir / summary_name).write_text(
            json.dumps(summary, indent=2), encoding="utf-8"
        )

        attack_rows = result_frame[result_frame["predicted_class"] != "Normal"].copy()
        attack_rows = attack_rows.sort_values("confidence", ascending=False).head(20)
        if attack_rows.empty:
            notable_rows = result_frame.sort_values("confidence", ascending=False).head(10)
        else:
            notable_rows = attack_rows

        charts = {
            "distribution": prediction_distribution(probabilities),
            "confidence": confidence_timeline(probabilities),
            "message_rate": message_rate_timeline(batch.metadata),
            "heatmap": probability_heatmap(probabilities),
        }

        return render_template(
            "results.html",
            run_id=run_id,
            summary=summary,
            charts=charts,
            notable_rows=notable_rows.to_dict(orient="records"),
            downloads=[csv_name, json_name, summary_name],
            warnings=registry.warnings,
        )

    @app.post("/api/predict")
    def api_predict():
        if not registry.available_models:
            return jsonify({"error": "No trained model artifacts were found."}), 503

        uploaded = request.files.get("can_file")
        if uploaded is None or uploaded.filename == "":
            return jsonify({"error": "Upload a CAN capture using field 'can_file'."}), 400
        if not allowed_file(uploaded.filename):
            return jsonify({"error": "Supported extensions: csv, txt, log."}), 400

        model_key = request.form.get("model_key", registry.default_model_key or "")
        available_keys = {item["key"] for item in registry.available_models}
        if model_key not in available_keys:
            return jsonify({"error": "Requested model is unavailable."}), 400

        run_id = uuid.uuid4().hex
        run_upload_dir = UPLOAD_DIR / run_id
        run_upload_dir.mkdir(parents=True, exist_ok=True)
        path = run_upload_dir / secure_filename(uploaded.filename)
        uploaded.save(path)

        try:
            batch = process_can_file(
                path,
                window_size=registry.expected_window_size,
                stride=registry.expected_window_size,
                max_windows=min(int(request.form.get("max_windows", 500)), MAX_WINDOWS),
            )
            probabilities = registry.predict(model_key, batch.features, batch.sequences)
            summary = summarise_predictions(probabilities)
            predictions = []
            for index in range(len(probabilities)):
                record, narrative = generate_incident_record(
                    probabilities[index],
                    batch.metadata.iloc[index],
                    model_name(model_key),
                    registry.expected_window_size,
                )
                record["narrative"] = narrative
                predictions.append(record)
            return jsonify({"summary": summary, "predictions": predictions})
        except Exception as exc:
            return jsonify({"error": str(exc)}), 500
        finally:
            shutil.rmtree(run_upload_dir, ignore_errors=True)

    @app.get("/download/<run_id>/<path:filename>")
    def download(run_id: str, filename: str):
        if not run_id.isalnum() or len(run_id) != 32:
            abort(404)
        directory = RESULT_DIR / run_id
        if not directory.exists():
            abort(404)
        return send_from_directory(directory, filename, as_attachment=True)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_large_upload(_error):
        return render_template(
            "error.html",
            title="File is too large",
            message=f"The maximum upload size is {MAX_UPLOAD_MB} MB.",
        ), 413

    @app.errorhandler(404)
    def not_found(_error):
        return render_template(
            "error.html",
            title="Page not found",
            message="The requested page or result file is unavailable.",
        ), 404

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug, use_reloader=False)
