import unittest
from unittest import mock
from app.models.user import User  # Assurez-vous que User est correctement importé
from app.models.place import Place  # Assurez-vous que Place est importé
from app.models.review import Review  # Assurez-vous que Review est importé

class TestUser(unittest.TestCase):

    def setUp(self):
        """Réinitialise les emails existants avant chaque test."""
        User.existing_emails.clear()

    def test_valid_user_creation(self):
        """Teste la création d'un utilisateur valide."""
        user = User("Alice", "Dupont", "alice.dupont@example.com")
        self.assertEqual(user.first_name, "Alice")
        self.assertEqual(user.last_name, "Dupont")
        self.assertEqual(user.email, "alice.dupont@example.com")
        self.assertFalse(user.is_admin)

    def test_invalid_first_name_empty(self):
        """Teste si un prénom vide déclenche une erreur."""
        with self.assertRaises(ValueError):
            User("", "Dupont", "alice.dupont@example.com")

    def test_invalid_first_name_too_long(self):
        """Teste si un prénom trop long déclenche une erreur."""
        with self.assertRaises(ValueError):
            User("A" * 51, "Dupont", "alice.dupont@example.com")

    def test_invalid_last_name_empty(self):
        """Teste si un nom de famille vide déclenche une erreur."""
        with self.assertRaises(ValueError):
            User("Alice", "", "alice.dupont@example.com")

    def test_invalid_last_name_too_long(self):
        """Teste si un nom de famille trop long déclenche une erreur."""
        with self.assertRaises(ValueError):
            User("Alice", "D" * 51, "alice.dupont@example.com")

    def test_invalid_email_format(self):
        """Teste si un email mal formé déclenche une erreur."""
        with self.assertRaises(ValueError):
            User("Alice", "Dupont", "alice.dupont.com")

    def test_duplicate_email(self):
        """Teste si la duplication d'email est interdite."""
        User("Alice", "Dupont", "alice.dupont@example.com")
        with self.assertRaises(ValueError):
            User("Bob", "Martin", "alice.dupont@example.com")

    def test_add_place(self):
        """Teste si un lieu peut être ajouté à l'utilisateur."""
        user = User("Alice", "Dupont", "alice.dupont@example.com")
        place_mock = mock.Mock(spec=Place)  # Spécifiez le mock pour Place
        user.add_place(place_mock)
        self.assertIn(place_mock, user.places)

    def test_add_review(self):
        """Teste si un avis peut être ajouté à l'utilisateur."""
        user = User("Alice", "Dupont", "alice.dupont@example.com")
        review_mock = mock.Mock(spec=Review)  # Spécifiez le mock pour Review
        user.add_review(review_mock)
        self.assertIn(review_mock, user.reviews)

if __name__ == '__main__':
    unittest.main()
# Exécutez le test avec: python3 -m unittest tests/test_user.py
                        # ou python3 -m pytest tests/test_user.py
