import unittest
from unittest import mock
from app.models.review import Review  # Assurez-vous que Review est correctement importé
from app.models.place import Place  # Assurez-vous que Place est importé
from app.models.user import User  # Assurez-vous que User est importé

class TestReview(unittest.TestCase):

    def test_valid_review_creation(self):
        """Teste la création d'un avis valide."""
        user_mock = mock.Mock(spec=User)
        place_mock = mock.Mock(spec=Place)
        review = Review("Great place!", 5, place_mock, user_mock)

        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.place, place_mock)
        self.assertEqual(review.user, user_mock)

    def test_invalid_text_empty(self):
        """Teste si un texte vide déclenche une erreur."""
        user_mock = mock.Mock(spec=User)
        place_mock = mock.Mock(spec=Place)
        with self.assertRaises(ValueError):
            Review("", 5, place_mock, user_mock)

    def test_invalid_rating_below_range(self):
        """Teste si une note en dessous de 1 déclenche une erreur."""
        user_mock = mock.Mock(spec=User)
        place_mock = mock.Mock(spec=Place)
        with self.assertRaises(ValueError):
            Review("Bad experience.", 0, place_mock, user_mock)

    def test_invalid_rating_above_range(self):
        """Teste si une note au-dessus de 5 déclenche une erreur."""
        user_mock = mock.Mock(spec=User)
        place_mock = mock.Mock(spec=Place)
        with self.assertRaises(ValueError):
            Review("Too good to be true!", 6, place_mock, user_mock)

    def test_invalid_place_type(self):
        """Teste si un mauvais type pour place déclenche une erreur."""
        user_mock = mock.Mock(spec=User)
        with self.assertRaises(TypeError):
            Review("Nice", 4, "not_a_place_instance", user_mock)

    def test_invalid_user_type(self):
        """Teste si un mauvais type pour user déclenche une erreur."""
        place_mock = mock.Mock(spec=Place)
        with self.assertRaises(TypeError):
            Review("Nice", 4, place_mock, "not_a_user_instance")

if __name__ == '__main__':
    unittest.main()
