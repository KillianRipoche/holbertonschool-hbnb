from app.api.v1.reviews import api as reviews_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.admin import api as admin_ns
from app.api.v1.users import api as users_ns
from app.api.v1.auth import api as auth_ns
from config import config
from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()


# Import namespaces from your API modules


def create_app(config_name='default'):
    app = Flask(__name__)
    app_config = config[config_name]
    app.config.from_object(app_config)

    # Initialize Flask-JWT-Extended
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
    jwt = JWTManager(app)

    # Initialize Flask-Restx API
    api = Api(app, version='1.0', title='Hbnb API', description='API for Hbnb')

    # Register namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(admin_ns, path='/api/v1/admin')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app


if __name__ == '__main__':
    application = create_app('development')
    application.run(host='0.0.0.0', port=5000)
