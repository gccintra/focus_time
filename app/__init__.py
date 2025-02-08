from flask import Flask
from app.routes.task_routes import task_bp
from app.routes.todo_routes import todo_bp  
from app.routes.error_routes import error_bp
from app.routes.home_routes import home_bp
from app.routes.auth_routes import auth_bp



def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'secret'

    app.register_blueprint(task_bp)  
    app.register_blueprint(todo_bp)  
    app.register_blueprint(error_bp)
    app.register_blueprint(home_bp)  
    app.register_blueprint(auth_bp)  

    return app
