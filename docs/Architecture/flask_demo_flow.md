# AutoSPECTRA Flask Demonstration Flow

## Demonstration Objective

Show a live, reproducible path from an unseen CAN log to a model prediction and incident report within the 5–7 minute demonstration allocation.

## Planned User Flow

1. Open the local AutoSPECTRA Flask dashboard.
2. Select a small unseen `.csv`, `.txt` or `.log` CAN capture.
3. Upload the file.
4. Validate the file format.
5. Parse CAN ID, DLC, payload and timestamps.
6. Build chronological 64-frame windows.
7. Run the selected model or calibrated fusion.
8. Display:
   - predicted class;
   - confidence;
   - per-class probabilities;
   - traffic statistics;
   - model inference time.
9. Generate a plain-language incident report.
10. Download window predictions and structured JSON/CSV reports.

## Planned Routes

```text
GET  /
GET  /health
POST /predict
POST /api/predict
GET  /download/<file>
```

## Minimum Dashboard Sections

- project title and defensive-use statement;
- upload form;
- selected model;
- parsing summary;
- class-distribution chart;
- probability chart;
- incident timeline;
- incident report;
- download links;
- human-oversight warning.

## Live Demonstration Script

```text
00:00–00:30  Open the application and identify the selected model.
00:30–01:15  Upload a small unseen CAN file.
01:15–02:00  Show parsing and windowing results.
02:00–03:15  Run inference and explain the class probabilities.
03:15–04:30  Show the incident report and traffic evidence.
04:30–05:15  Download CSV or JSON results.
05:15–06:00  Explain limitations, ethics and human oversight.
```

## Reliability Controls

- use a local server;
- pre-install dependencies;
- pre-load trained models;
- use a small test file;
- avoid internet dependency;
- provide a Random Forest fallback;
- validate the demo on the presentation laptop;
- keep a second unseen test file;
- do not rely only on screenshots or video.

## Safety Position

The Flask application is an academic monitoring and decision-support prototype. It must not automatically isolate an ECU or control braking, steering, engine, transmission or other safety-critical vehicle functions.
