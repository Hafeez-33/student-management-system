import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Local: 127.0.0.1:5000 with debug. Render/Gunicorn binds 0.0.0.0:$PORT itself.
    port = int(os.environ.get("PORT", "5000"))
    hosted = "PORT" in os.environ
    app.run(
        host="0.0.0.0" if hosted else "127.0.0.1",
        port=port,
        debug=not hosted,
    )
