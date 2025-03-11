import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_api
from app.services import facade


class TestUsersAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a Flask test client
        app = Flask(__name__)
        api = Api(app)
        api.add_namespace(users_api, path='/api/v1/users')

        @app.route('/health')
        def health_check():
            return "OK", 200

        # Use a testing database or mock services if needed
        app.config['TESTING'] = True
        cls.client = app.test_client()

    @patch.object(facade, 'create_user')
    def test_create_user(self, mock_create_user):
        # Mock the facade call to create a user
        mock_user = MagicMock()
        mock_user.id = "123"
        mock_user.username = "testuser"
        mock_user.email = "testuser@example.com"
        mock_create_user.return_value = mock_user

        # Send POST request to create a new user
        response = self.client.post('/api/v1/users', json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "id": "123",
            "username": "testuser",
            "email": "testuser@example.com"
        })

    @patch.object(facade, 'get_all_users')
    def test_get_all_users(self, mock_get_all_users):
        # Mock the facade call to get all users
        mock_users = [
            {"id": "123", "username": "testuser1", "email": "testuser1@example.com"},
            {"id": "124", "username": "testuser2", "email": "testuser2@example.com"}
        ]
        mock_get_all_users.return_value = mock_users

        # Send GET request to retrieve all users
        response = self.client.get('/api/v1/users')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]["username"], "testuser1")
        self.assertEqual(response.json[1]["email"], "testuser2@example.com")

    @patch.object(facade, 'get_user')
    def test_get_user_by_id(self, mock_get_user):
        # Mock the facade call to get a user by ID
        mock_user = {"id": "123", "username": "testuser", "email": "testuser@example.com"}
        mock_get_user.return_value = mock_user

        # Send GET request to retrieve user by ID
        response = self.client.get('/api/v1/users/123')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["id"], "123")
        self.assertEqual(response.json["username"], "testuser")

    @patch.object(facade, 'update_user')
    def test_update_user(self, mock_update_user):
        # Mock the facade call update a user
        mock_user = {"id": "123", "username": "updateduser", "email": "updateduser@example.com"}
        mock_update_user.return_value = mock_user

        # Send PUT request to update the user
        response = self.client.put('/api/v1/users/123', json={
            "username": "updateduser",
            "email": "updateduser@example.com"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["username"], "updateduser")
        self.assertEqual(response.json["email"], "updateduser@example.com")

    @patch.object(facade, 'delete_user')
    def test_delete_user(self, mock_delete_user):
        # Mock the facade call to delete a user
        mock_delete_user.return_value = True

        # Send DELETE request to delete the user
        response = self.client.delete('/api/v1/users/123')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "User deleted successfully"})


if __name__ == '__main__':
    unittest.main()
