from flask import Flask
from app.config import Config
from app.routes.analyze import analyze_bp
from app.routes.results import results_bp

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(analyze_bp)
    app.register_blueprint(results_bp)
    return app
