from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app import facade

api = Namespace('admin', description='Admin operations')


@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')
        password = data.get('password')

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        try:
            updated_user = facade.update_user(user_id=user_id, email=email, password=password)
            return {'message': 'User updated successfully', 'user': updated_user.to_dict()}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')
        password = user_data.get('password')
        is_admin = user_data.get('is_admin', False)

        if not email or not password:
            return {'error': 'Missing required fields'}, 400

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        try:
            user = facade.create_user(email=email, password=password, is_admin=is_admin)
            return {'message': 'User created', 'user': user.to_dict()}, 201
        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        name = data.get('name')
        if not name:
            return {'error': 'Missing amenity name'}, 400

        try:
            amenity = facade.create_amenity(name=name)
            return {'message': 'Amenity created', 'amenity': amenity.to_dict()}, 201
        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        name = data.get('name')
        if not name:
            return {'error': 'Missing amenity name'}, 400

        try:
            updated_amenity = facade.update_amenity(amenity_id=amenity_id, name=name)
            return {'message': 'Amenity updated', 'amenity': updated_amenity.to_dict()}, 200
        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        data = request.json
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')

        try:
            updated_place = facade.update_place(place_id=place_id, name=name, description=description, price=price)
            return {'message': 'Place updated', 'place': updated_place.to_dict()}, 200
        except Exception as e:
            return {'error': str(e)}, 500
