"""Launch AutoSPECTRA Flask in Kaggle through an ngrok tunnel."""
from __future__ import annotations

import os
import threading
import time

from pyngrok import ngrok

from app import app

PORT = int(os.getenv("PORT", "5000"))
TOKEN = os.getenv("NGROK_AUTHTOKEN")

if not TOKEN:
    raise RuntimeError(
        "Set NGROK_AUTHTOKEN in a Kaggle secret or environment variable before running."
    )

ngrok.set_auth_token(TOKEN)

thread = threading.Thread(
    target=lambda: app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False,
        use_reloader=False,
    ),
    daemon=True,
)
thread.start()
time.sleep(2)

public_url = ngrok.connect(PORT, bind_tls=True).public_url
print("AutoSPECTRA public URL:", public_url)
print("Keep this process running while you use the application.")

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    ngrok.kill()
