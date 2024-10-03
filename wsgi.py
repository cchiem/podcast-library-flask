"""App entry point."""
import os
from podcast import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use the port defined by Render, fallback to 5000 locally
    app.run(host="0.0.0.0", port=port, threaded=False)
