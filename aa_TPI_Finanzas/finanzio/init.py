from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()

# Inicializaciones
db = SQLAlchemy()
bcrypt = Bcrypt()
csrf = CSRFProtect()

# Función principal
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv("SECRET_KEY")
    app.config['WTF_CSRF_ENABLED'] = True  
    #Inicializar con la App
    db.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app) 
    
    #Registrar Blueprints
    from views.view import bp
    app.register_blueprint(bp)
    from views.auth import auth_bp
    app.register_blueprint(auth_bp)
    from views.user import user_bp
    app.register_blueprint(user_bp)

    #Manejo de errores    
    @app.errorhandler(401)
    def custom_401(error):
         return jsonify({"msg": "Token inválido o expirado"}), 401

    @app.errorhandler(422)
    def custom_422(error):
        return jsonify({"msg": "Token mal formado"}), 422

    return app
