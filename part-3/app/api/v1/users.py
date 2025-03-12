from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
<<<<<<< HEAD
import os
=======
>>>>>>> d0374826fa7d65b2c619775477fd8b5ed77c5387
from app.services import facade
from config import config

api = Namespace('users', description='User operations')

<<<<<<< HEAD
# Define the user model for documentation and validation
=======
# Definition of the user model, including password for validation and documentation
>>>>>>> d0374826fa7d65b2c619775477fd8b5ed77c5387
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
        If "admin_secret" matches config['default'].ADMIN_SECRET, the user is created with admin privileges.
        """
        user_data = api.payload

        # Check if the email is already registered
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

<<<<<<< HEAD
        # Determine if the account should be admin based on the provided admin_secret
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

=======
        # Call create_user to hash the password (via facade service)
        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201
>>>>>>> d0374826fa7d65b2c619775477fd8b5ed77c5387

@api.route('/all')
class AllUsersList(Resource):
    @api.response(200, 'List of all users retrieved successfully')
    @api.response(404, 'No users found')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        if not users:
            return {'message': 'No users found'}, 404

        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            for user in users
        ], 200

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
    @api.response(200, 'User details updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
<<<<<<< HEAD
        """
        Update a user's own details.
        The authenticated user must match the user_id (admin changes must be done via admin endpoints).
        """
        current_user = get_jwt_identity()
        if current_user['id'] != user_id:
            return {'message': 'Unauthorized action'}, 403

        user_data = api.payload
        # Remove admin_secret from payload (not used here)
        user_data.pop('admin_secret', None)

=======
        """Update user details"""
        # Get the current user's identity from the JWT
        current_user = get_jwt_identity()

        # Ensure the current user is trying to update their own data
        if current_user['id'] != user_id:
            return {'message': 'Unauthorized action'}, 403  # User cannot update someone else's data

        user_data = api.payload
>>>>>>> d0374826fa7d65b2c619775477fd8b5ed77c5387
        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
<<<<<<< HEAD
                'email': updated_user.email,
                'is_admin': updated_user.is_admin
=======
                'email': updated_user.email
>>>>>>> d0374826fa7d65b2c619775477fd8b5ed77c5387
            }, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, user_id):
<<<<<<< HEAD
        """
        Delete a user account.
        A user can delete their own account.
        (For admin deletion of any user, use the admin endpoint.)
        """
        current_user = get_jwt_identity()
        if current_user['id'] != user_id:
            return {'message': 'Unauthorized action'}, 403
=======
        """Delete user account"""
        # Get the current user's identity from the JWT
        current_user = get_jwt_identity()

        # Ensure the current user is trying to delete their own account
        if current_user['id'] != user_id:
            return {'message': 'Unauthorized action'}, 403  # User cannot delete someone else's account
>>>>>>> d0374826fa7d65b2c619775477fd8b5ed77c5387

        deleted_user = facade.delete_user(user_id)
        if not deleted_user:
            return {'error': 'User not found'}, 404
        return {'message': 'User deleted successfully'}, 200
