from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db import DATABASE_URL
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt=Bcrypt()
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.secret_key=os.getenv("SECRET_KEY")
    db.init_app(app)
    bcrypt.init_app(app)
    from view import bp
    app.register_blueprint(bp)
    
    return app