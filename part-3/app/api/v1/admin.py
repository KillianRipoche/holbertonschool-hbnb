from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from functools import wraps
from app.services import facade

api = Namespace('admin', description='Admin operations')

def admin_required(fn):
    """Décorateur pour vérifier que l'utilisateur a les privilèges administrateur."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        return fn(*args, **kwargs)
    return wrapper

@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    @admin_required
    def put(self, user_id):
        data = request.json
        # Vérification de l'email si fourni
        if "email" in data:
            existing_user = facade.get_user_by_email(data["email"])
            if existing_user and str(existing_user.id) != str(user_id):
                return {'error': 'Email is already in use'}, 400

        try:
            updated_user = facade.update_user(user_id, data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return {
                'message': 'User updated successfully',
                'user': updated_user.to_dict()
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    @admin_required
    def post(self):
        data = request.json
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return {'error': f'Missing required field: {field}'}, 400

        if facade.get_user_by_email(data["email"]):
            return {'error': 'Email already registered'}, 400

        try:
            user = facade.create_user(data)
            return {
                'message': 'User created',
                'user': user.to_dict()
            }, 201
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    @admin_required
    def post(self):
        data = request.json
        if "name" not in data or not data["name"]:
            return {'error': 'Missing amenity name'}, 400

        try:
            amenity = facade.create_amenity(data)
            return {
                'message': 'Amenity created',
                'amenity': {
                    'id': amenity.id,
                    'name': amenity.name
                }
            }, 201
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    @admin_required
    def put(self, amenity_id):
        data = request.json
        if "name" not in data or not data["name"]:
            return {'error': 'Missing amenity name'}, 400

        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404
            return {
                'message': 'Amenity updated',
                'amenity': {
                    'id': updated_amenity.id,
                    'name': updated_amenity.name
                }
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    @admin_required
    def put(self, place_id):
        data = request.json
        # Pour simplifier, on attend un dictionnaire avec les champs à mettre à jour
        try:
            updated_place = facade.update_place(place_id, data)
            if not updated_place:
                return {'error': 'Place not found'}, 404
            return {
                'message': 'Place updated',
                'place': updated_place.to_dict()
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500
