import unittest
from app.services.facade import HBnBFacade
from app.models.user import User

class TestHBnBFacade(unittest.TestCase):
    def setUp(self):
        # Vider l'ensemble des emails avant chaque test
        User.existing_emails.clear()

        self.facade = HBnBFacade()
        # Créer un utilisateur par défaut, si nécessaire
        self.user_data = {
            "first_name": "Alice",
            "last_name": "Doe",
            "email": "alice@example.com"
        }
        self.user = self.facade.create_user(self.user_data)

    # ---------- Tests pour les USERS ----------
    def test_create_user(self):
        new_user_data = {
            "first_name": "Bob",
            "last_name": "Marley",
            "email": "bob@example.com"
        }
        new_user = self.facade.create_user(new_user_data)
        self.assertIn("id", new_user)
        self.assertEqual(new_user["email"], "bob@example.com")

    def test_create_user_duplicate_email(self):
        duplicate_user_data = {
            "first_name": "Alice2",
            "last_name": "Doe2",
            "email": "alice@example.com"  # même email que self.user
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_user(duplicate_user_data)
        self.assertIn("Cet email est déjà utilisé", str(context.exception))

    # ---------- Tests pour les AMENITIES ----------
    def test_create_amenity_valid(self):
        amenity_data = {"name": "Pool"}
        amenity = self.facade.create_amenity(amenity_data)
        self.assertIn("id", amenity)
        self.assertEqual(amenity["name"], "Pool")

    def test_create_amenity_invalid(self):
        amenity_data = {"name": ""}
        with self.assertRaises(ValueError) as context:
            self.facade.create_amenity(amenity_data)
        self.assertIn("non-empty", str(context.exception))

    def test_update_amenity(self):
        amenity = self.facade.create_amenity({"name": "Garden"})
        updated = self.facade.update_amenity(amenity["id"], {"name": "Big Garden"})
        self.assertEqual(updated["name"], "Big Garden")

    def test_get_all_amenities(self):
        self.facade.create_amenity({"name": "Pool"})
        self.facade.create_amenity({"name": "WiFi"})
        amenities = self.facade.get_all_amenities()
        self.assertTrue(len(amenities) >= 2)

    # ---------- Tests pour les PLACES ----------
    def test_create_place_valid(self):
        place_data = {
            "title": "Central Apartment",
            "description": "Nice place in city center",
            "price": 150.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user["id"],
            "amenities": []
        }
        place = self.facade.create_place(place_data)
        self.assertIn("id", place)
        self.assertEqual(place["title"], "Central Apartment")

    def test_create_place_invalid_price(self):
        place_data = {
            "title": "Cheap Apartment",
            "description": "Negative price test",
            "price": -50.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user["id"],
            "amenities": []
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_place(place_data)
        self.assertIn("non-negative", str(context.exception))

    def test_update_place(self):
        place_data = {
            "title": "Old Title",
            "description": "Old description",
            "price": 100.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user["id"],
            "amenities": []
        }
        place = self.facade.create_place(place_data)
        updated = self.facade.update_place(place["id"], {"title": "New Title", "price": 120.0})
        self.assertEqual(updated["title"], "New Title")
        self.assertEqual(updated["price"], 120.0)

    def test_get_place_not_found(self):
        with self.assertRaises(ValueError) as context:
            self.facade.get_place("non-existent-id")
        self.assertIn("Place not found", str(context.exception))

    def test_get_all_places(self):
        self.facade.create_place({
            "title": "Apartment 1",
            "description": "First apartment",
            "price": 100.0,
            "latitude": 40.0,
            "longitude": 3.0,
            "owner_id": self.user["id"],
            "amenities": []
        })
        self.facade.create_place({
            "title": "Apartment 2",
            "description": "Second apartment",
            "price": 200.0,
            "latitude": 41.0,
            "longitude": 4.0,
            "owner_id": self.user["id"],
            "amenities": []
        })
        places = self.facade.get_all_places()
        self.assertTrue(len(places) >= 2)

    # ---------- Tests pour les REVIEWS ----------
    def test_create_review_valid(self):
        place_data = {
            "title": "Review Place",
            "description": "Place for reviews",
            "price": 150.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user["id"],
            "amenities": []
        }
        place = self.facade.create_place(place_data)
        review_data = {
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user["id"],
            "place_id": place["id"]
        }
        review = self.facade.create_review(review_data)
        self.assertIn("id", review)
        self.assertEqual(review["text"], "Great place!")

    def test_create_review_invalid_rating(self):
        place_data = {
            "title": "Review Place 2",
            "description": "Place for reviews",
            "price": 150.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user["id"],
            "amenities": []
        }
        place = self.facade.create_place(place_data)
        review_data = {
            "text": "Bad rating",
            "rating": 6,  # invalide
            "user_id": self.user["id"],
            "place_id": place["id"]
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_review(review_data)
        self.assertIn("between 1 and 5", str(context.exception))

    def test_update_review(self):
        place_data = {
            "title": "Review Update Place",
            "description": "Place for review update",
            "price": 150.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user["id"],
            "amenities": []
        }
        place = self.facade.create_place(place_data)
        review_data = {
            "text": "Initial review",
            "rating": 3,
            "user_id": self.user["id"],
            "place_id": place["id"]
        }
        review = self.facade.create_review(review_data)
        updated = self.facade.update_review(review["id"], {"text": "Updated review", "rating": 4})
        self.assertEqual(updated["text"], "Updated review")
        self.assertEqual(updated["rating"], 4)

    def test_delete_review(self):
        place_data = {
            "title": "Review Delete Place",
            "description": "Place for review deletion",
            "price": 150.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user["id"],
            "amenities": []
        }
        place = self.facade.create_place(place_data)
        review_data = {
            "text": "Review to delete",
            "rating": 3,
            "user_id": self.user["id"],
            "place_id": place["id"]
        }
        review = self.facade.create_review(review_data)
        deleted = self.facade.delete_review(review["id"])
        self.assertEqual(deleted["id"], review["id"])
        # Après suppression, get_review doit renvoyer None
        self.assertIsNone(self.facade.get_review(review["id"]))

    def test_get_reviews_by_place(self):
        place_data1 = {
            "title": "Place 1",
            "description": "First place",
            "price": 100.0,
            "latitude": 40.0,
            "longitude": 3.0,
            "owner_id": self.user["id"],
            "amenities": []
        }
        place_data2 = {
            "title": "Place 2",
            "description": "Second place",
            "price": 200.0,
            "latitude": 41.0,
            "longitude": 4.0,
            "owner_id": self.user["id"],
            "amenities": []
        }
        place1 = self.facade.create_place(place_data1)
        place2 = self.facade.create_place(place_data2)
        review_data1 = {
            "text": "Review for place1",
            "rating": 5,
            "user_id": self.user["id"],
            "place_id": place1["id"]
        }
        review_data2 = {
            "text": "Another review for place1",
            "rating": 4,
            "user_id": self.user["id"],
            "place_id": place1["id"]
        }
        review_data3 = {
            "text": "Review for place2",
            "rating": 3,
            "user_id": self.user["id"],
            "place_id": place2["id"]
        }
        self.facade.create_review(review_data1)
        self.facade.create_review(review_data2)
        self.facade.create_review(review_data3)
        reviews_place1 = self.facade.get_reviews_by_place(place1["id"])
        reviews_place2 = self.facade.get_reviews_by_place(place2["id"])
        self.assertEqual(len(reviews_place1), 2)
        self.assertEqual(len(reviews_place2), 1)

if __name__ == "__main__":
    unittest.main()
