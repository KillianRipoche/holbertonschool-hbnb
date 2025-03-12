from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from config import config

api = Namespace('users', description='User operations')

# Model for user registration
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'admin_secret': fields.String(required=False, description='Secret to create an admin account')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input data')
    def post(self):
        """
        Self-registration: Create a new user.
        If "admin_secret" matches config['default'].ADMIN_SECRET, the user is created as an admin.
        """
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        admin_secret = user_data.pop('admin_secret', None)
        if admin_secret and admin_secret == config['default'].ADMIN_SECRET:
            user_data['is_admin'] = True
        else:
            user_data['is_admin'] = False

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'is_admin': new_user.is_admin
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Retrieve user details by ID.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200

    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        """
        Update a user's own details.
        The authenticated user must match the user_id.
        """
        current_user = get_jwt_identity()
        if current_user['id'] != user_id:
            return {'message': 'Unauthorized action'}, 403

        user_data = api.payload
        user_data.pop('admin_secret', None)
        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'is_admin': updated_user.is_admin
            }, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, user_id):
        """
        Delete a user account.
        A user can delete their own account.
        (For admin deletion of any user, use the admin endpoint.)
        """
        current_user = get_jwt_identity()
        if current_user['id'] != user_id:
            return {'message': 'Unauthorized action'}, 403

        deleted_user = facade.delete_user(user_id)
        if not deleted_user:
            return {'error': 'User not found'}, 404
        return {'message': 'User deleted successfully'}, 200
