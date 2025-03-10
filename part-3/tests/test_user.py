import unittest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
import pytest
import bcrypt


class TestUser(unittest.TestCase):

    def setUp(self):
        # Réinitialise les emails utilisés avant chaque test
        User.existing_emails = set()

    def test_valid_user_creation(self):
        """Tests the creation of a valid user."""
        user = User("Alice", "Dupont", "alice.dupont@example.com", "Password123$")
        self.assertEqual(user.first_name, "Alice")
        self.assertEqual(user.last_name, "Dupont")
        self.assertEqual(user.email, "alice.dupont@example.com")

    def test_invalid_first_name_empty(self):
        """Tests if an empty first name triggers an error."""
        with self.assertRaises(ValueError):
            User("", "Dupont", "alice2@example.com", "Password123$")

    def test_invalid_first_name_too_long(self):
        """Test if a first name that is too long triggers an error."""
        with self.assertRaises(ValueError):
            User("A" * 51, "Dupont", "alice3@example.com", "Password123$")

    def test_invalid_last_name_empty(self):
        """Tests if an empty last name triggers an error."""
        with self.assertRaises(ValueError):
            User("Alice", "", "alice4@example.com", "Password123$")

    def test_invalid_last_name_too_long(self):
        """Tests if a last name that is too long triggers an error."""
        with self.assertRaises(ValueError):
            User("Alice", "D" * 51, "alice5@example.com", "Password123$")

    def test_invalid_email_format(self):
        """Tests if a malformed email triggers an error."""
        with self.assertRaises(ValueError):
            User("Alice", "Dupont", "alice6.example.com", "Password123$")

    def test_duplicate_email(self):
        """Tests if email duplication is prohibited."""
        User("Alice", "Dupont", "alice7@example.com", "Password123$")
        with self.assertRaises(ValueError):
            User("Bob", "Martin", "alice7@example.com", "Password456$")

    def test_add_place(self):
        """Test if a location can be added to the user."""
        user = User("Alice", "Dupont", "alice8@example.com", "Password123$")
        place = Place("Paris", "A nice place", 48.8566, 2.3522, user)  # Correction: ajout des arguments requis
        self.assertEqual(place.owner, user)
        self.assertEqual(place.name, "Paris")

    def test_add_review(self):
        """Tests if a notice can be added to the user."""
        user = User("Alice", "Dupont", "alice9@example.com", "Password123$")
        place = Place("Paris", "A nice place", 48.8566, 2.3522, user)  # Correction: ajout des arguments requis
        review = Review("Great place!", user, place)
        self.assertEqual(review.user, user)
        self.assertEqual(review.place, place)

    def test_password_hashing_and_checking():
        password = "Password123$"
        user = User("Alice", password)

        # Vérification du mot de passe
        assert user.check_password("Password123$") == True
        assert user.check_password("WrongPassword") == False
