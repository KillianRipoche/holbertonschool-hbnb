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

    def test_create_user_invalid_first_name(self):
        """
        Si ta classe User vérifie que first_name ne doit pas être vide ou trop long,
        on peut tester un first_name vide.
        """
        invalid_data = {
            "first_name": "",
            "last_name": "Test",
            "email": "invalid@example.com"
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_user(invalid_data)
        self.assertIn("first_name invalide", str(context.exception))

    def test_create_user_invalid_last_name(self):
        """
        Si ta classe User vérifie last_name,
        on teste un last_name vide ou trop long.
        """
        invalid_data = {
            "first_name": "Bob",
            "last_name": "",
            "email": "invalid@example.com"
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_user(invalid_data)
        self.assertIn("last_name invalide", str(context.exception))

    def test_create_user_invalid_email_format(self):
        """
        Si ta classe User vérifie le format d'email,
        on teste un email sans '@' ni '.'
        """
        invalid_data = {
            "first_name": "Charlie",
            "last_name": "Brown",
            "email": "not_an_email"
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_user(invalid_data)
        self.assertIn("Format d'email invalide", str(context.exception))

    # ---------- Tests pour les PLACES ----------
    def test_create_place_invalid_latitude_high(self):
        """
        Test de création d'un place avec latitude > 90
        On attend une ValueError "Latitude must be between -90 and 90."
        """
        place_data = {
            "title": "Out of Bounds Latitude",
            "description": "Latitude > 90",
            "price": 50.0,
            "latitude": 91.0,  # invalide
            "longitude": 2.3522,
            "owner_id": self.user["id"],
            "amenities": []
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_place(place_data)
        self.assertIn("Latitude must be between -90 and 90", str(context.exception))

    def test_create_place_invalid_latitude_low(self):
        """
        Test de création d'un place avec latitude < -90
        """
        place_data = {
            "title": "Out of Bounds Latitude",
            "description": "Latitude < -90",
            "price": 50.0,
            "latitude": -91.0,
            "longitude": 2.3522,
            "owner_id": self.user["id"],
            "amenities": []
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_place(place_data)
        self.assertIn("Latitude must be between -90 and 90", str(context.exception))

    def test_create_place_invalid_longitude_high(self):
        """
        Test de création d'un place avec longitude > 180
        """
        place_data = {
            "title": "Out of Bounds Longitude",
            "description": "Longitude > 180",
            "price": 50.0,
            "latitude": 48.8566,
            "longitude": 181.0,  # invalide
            "owner_id": self.user["id"],
            "amenities": []
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_place(place_data)
        self.assertIn("Longitude must be between -180 and 180", str(context.exception))

    def test_create_place_invalid_longitude_low(self):
        """
        Test de création d'un place avec longitude < -180
        """
        place_data = {
            "title": "Out of Bounds Longitude",
            "description": "Longitude < -180",
            "price": 50.0,
            "latitude": 48.8566,
            "longitude": -181.0,  # invalide
            "owner_id": self.user["id"],
            "amenities": []
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_place(place_data)
        self.assertIn("Longitude must be between -180 and 180", str(context.exception))

    def test_create_place_no_owner(self):
        """
        Test de création d'un place sans owner existant
        On attend une ValueError "Owner not found."
        """
        place_data = {
            "title": "No Owner",
            "description": "Testing place with non-existent owner",
            "price": 50.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": "non-existent-id",  # invalide
            "amenities": []
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_place(place_data)
        self.assertIn("Owner not found", str(context.exception))

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

    def test_create_review_missing_text(self):
        """
        Test de création de review sans champ 'text'
        On attend "Missing required field: text"
        """
        place_data = self.facade.create_place({
            "title": "Missing text place",
            "description": "desc",
            "price": 100.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user["id"],
            "amenities": []
        })
        review_data = {
            # "text": "No text provided", # manquant
            "rating": 4,
            "user_id": self.user["id"],
            "place_id": place_data["id"]
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_review(review_data)
        self.assertIn("Missing required field: text", str(context.exception))

    def test_create_review_missing_rating(self):
        """
        Test de création de review sans champ 'rating'
        """
        place_data = self.facade.create_place({
            "title": "Missing rating place",
            "description": "desc",
            "price": 100.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user["id"],
            "amenities": []
        })
        review_data = {
            "text": "No rating provided",
            # "rating": 4, # manquant
            "user_id": self.user["id"],
            "place_id": place_data["id"]
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_review(review_data)
        self.assertIn("Missing required field: rating", str(context.exception))

    def test_create_review_no_user(self):
        """
        Test de création de review avec user_id inexistant
        """
        place_data = self.facade.create_place({
            "title": "No user place",
            "description": "desc",
            "price": 100.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.user["id"],
            "amenities": []
        })
        review_data = {
            "text": "User not found test",
            "rating": 4,
            "user_id": "non-existent-id",  # invalide
            "place_id": place_data["id"]
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_review(review_data)
        self.assertIn("User not found", str(context.exception))

    def test_create_review_no_place(self):
        """
        Test de création de review avec place_id inexistant
        """
        review_data = {
            "text": "Place not found test",
            "rating": 4,
            "user_id": self.user["id"],
            "place_id": "non-existent-id"
        }
        with self.assertRaises(ValueError) as context:
            self.facade.create_review(review_data)
        self.assertIn("Place not found", str(context.exception))

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
