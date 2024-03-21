from flask import Flask
from app.extentions import db,migrate


# application  factory function

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    
    db.init_app(app)
    migrate.init_app(app,db)
    
    
    @app.route("/")
    def home():
        return "Authors API project setup 1"
    
    
    return app