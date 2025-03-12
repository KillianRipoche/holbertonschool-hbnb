import os
from dotenv import load_dotenv
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from config import DevelopmentConfig

# Import des namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.admin import api as admin_ns

bcrypt = Bcrypt()
jwt = JWTManager()

# Configuration de l'authentification Swagger
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Enter 'Bearer <JWT>'"
    }
}

def create_app(config_class="config.DevelopmentConfig"):
    # Charger les variables d'environnement depuis .env (si présent)
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialiser bcrypt et JWT
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Associer la clé JWT à la SECRET_KEY de la config
    # (si tu veux explicitement la configurer)
    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY', 'my_flask_session_key')

    # Initialiser l'API Flask-Restx
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        authorizations=authorizations,
        security='Bearer'
    )

    # Enregistrer les namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(admin_ns, path='/api/v1/admin')

    return app
