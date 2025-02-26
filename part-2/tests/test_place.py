import unittest
from unittest import mock
from app.models.place import Place  # Assurez-vous que Place est correctement importé
from app.models.user import User  # Assurez-vous que User est importé
from app.models.review import Review  # Assurez-vous que Review est importé
from app.models.amenity import Amenity  # Assurez-vous que Amenity est importé

class TestPlace(unittest.TestCase):

    def test_valid_place_creation(self):
        """Teste la création d'un lieu valide."""
        owner_mock = mock.Mock(spec=User)
        place = Place("Cozy Cabin", "A small cozy cabin in the woods", 120.0, 45.0, -73.0, owner_mock)

        self.assertEqual(place.title, "Cozy Cabin")
        self.assertEqual(place.description, "A small cozy cabin in the woods")
        self.assertEqual(place.price, 120.0)
        self.assertEqual(place.latitude, 45.0)
        self.assertEqual(place.longitude, -73.0)
        self.assertEqual(place.owner, owner_mock)
        self.assertEqual(place.reviews, [])
        self.assertEqual(place.amenities, [])

    def test_invalid_title_empty(self):
        """Teste si un titre vide déclenche une erreur."""
        owner_mock = mock.Mock(spec=User)
        with self.assertRaises(ValueError):
            Place("", "Description", 50.0, 40.0, -75.0, owner_mock)

    def test_invalid_title_too_long(self):
        """Teste si un titre trop long déclenche une erreur."""
        owner_mock = mock.Mock(spec=User)
        with self.assertRaises(ValueError):
            Place("T" * 101, "Description", 50.0, 40.0, -75.0, owner_mock)

    def test_invalid_price_negative(self):
        """Teste si un prix négatif déclenche une erreur."""
        owner_mock = mock.Mock(spec=User)
        with self.assertRaises(ValueError):
            Place("Nice Place", "Description", -10.0, 40.0, -75.0, owner_mock)

    def test_invalid_latitude_out_of_bounds(self):
        """Teste si une latitude hors limites déclenche une erreur."""
        owner_mock = mock.Mock(spec=User)
        with self.assertRaises(ValueError):
            Place("Nice Place", "Description", 100.0, -91.0, -75.0, owner_mock)

    def test_invalid_longitude_out_of_bounds(self):
        """Teste si une longitude hors limites déclenche une erreur."""
        owner_mock = mock.Mock(spec=User)
        with self.assertRaises(ValueError):
            Place("Nice Place", "Description", 100.0, 40.0, 181.0, owner_mock)

    def test_invalid_owner_type(self):
        """Teste si un mauvais type pour owner déclenche une erreur."""
        with self.assertRaises(TypeError):
            Place("Nice Place", "Description", 100.0, 40.0, -75.0, "not_a_user_instance")

    def test_add_review(self):
        """Teste l'ajout d'un avis à un lieu."""
        owner_mock = mock.Mock(spec=User)
        review_mock = mock.Mock(spec=Review)
        place = Place("Nice Place", "Description", 100.0, 40.0, -75.0, owner_mock)

        place.add_review(review_mock)
        self.assertIn(review_mock, place.reviews)

    def test_add_review_invalid_type(self):
        """Teste si un mauvais type d'avis déclenche une erreur."""
        owner_mock = mock.Mock(spec=User)
        place = Place("Nice Place", "Description", 100.0, 40.0, -75.0, owner_mock)

        with self.assertRaises(TypeError):
            place.add_review("not_a_review_instance")

    def test_add_amenity(self):
        """Teste l'ajout d'une commodité à un lieu."""
        owner_mock = mock.Mock(spec=User)
        amenity_mock = mock.Mock(spec=Amenity)
        place = Place("Nice Place", "Description", 100.0, 40.0, -75.0, owner_mock)

        place.add_amenity(amenity_mock)
        self.assertIn(amenity_mock, place.amenities)

    def test_add_amenity_invalid_type(self):
        """Teste si un mauvais type de commodité déclenche une erreur."""
        owner_mock = mock.Mock(spec=User)
        place = Place("Nice Place", "Description", 100.0, 40.0, -75.0, owner_mock)

        with self.assertRaises(TypeError):
            place.add_amenity("not_an_amenity_instance")

if __name__ == '__main__':
    unittest.main()
