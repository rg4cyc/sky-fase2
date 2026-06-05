"""Punto de entrada de la aplicación Flask Sky Fase 2."""

from flask import Flask

from app.routes import api


def create_app() -> Flask:
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__)
    app.register_blueprint(api)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
