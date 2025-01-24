from flask import Flask
from app.routes.task_routes import task_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(task_bp)  
    return app
