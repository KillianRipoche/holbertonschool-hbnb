import os
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

# Ajout d'un champ optionnel "admin_secret" dans le modèle
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
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
        Si le champ "admin_secret" est fourni et correct, l'utilisateur sera créé avec les privilèges administrateur.
        """
        user_data = api.payload

        # Vérifier si l'email est déjà enregistré
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Détermine le niveau de privilège
        admin_secret = user_data.pop("admin_secret", None)
        # On compare avec la valeur stockée dans l'environnement (à définir, par exemple, dans un fichier .env)
        if admin_secret and admin_secret == os.getenv("ADMIN_SECRET"):
            user_data["is_admin"] = True
        else:
            user_data["is_admin"] = False

        try:
            # Création de l'utilisateur via la façade
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

@api.route('/all')
class AllUsersList(Resource):
    @api.response(200, 'List of all users retrieved successfully')
    @api.response(404, 'No users found')
    def get(self):
        """
        Retrieve all users.
        """
        users = facade.get_all_users()
        if not users:
            return {'message': 'No users found'}, 404

        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_admin': user.is_admin
            }
            for user in users
        ], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Get user details by ID.
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
        """
        Update user's own details.
        Seul l'utilisateur lui-même peut modifier ses informations.
        """
        current_user = get_jwt_identity()

        if current_user['id'] != user_id:
            return {'message': 'Unauthorized action'}, 403

        user_data = api.payload
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
        Delete user's own account.
        """
        current_user = get_jwt_identity()

        if not (current_user.get('is_admin') or current_user['id'] == user_id):
            return {'message': 'Unauthorized action'}, 403

        deleted_user = facade.delete_user(user_id)
        if not deleted_user:
            return {'error': 'User not found'}, 404
        return {'message': 'User deleted successfully'}, 200
