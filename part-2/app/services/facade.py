from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def _user_to_dict(self, user_obj):
        if not user_obj:
            return None
        return {
            "id": user_obj.id,
            "first_name": user_obj.first_name,
            "last_name": user_obj.last_name,
            "email": user_obj.email
        }

    def _amenity_to_dict(self, amenity_obj):
        if not amenity_obj:
            return None
        return {
            "id": amenity_obj.id,
            "name": amenity_obj.name
        }

    def _place_to_dict(self, place_obj):
        if not place_obj:
            return None
        return {
            "id": place_obj.id,
            "title": place_obj.title,
            "description": place_obj.description,
            "price": place_obj.price,
            "latitude": place_obj.latitude,
            "longitude": place_obj.longitude,
            "owner_id": place_obj.owner.id,
            "amenities": [a.id for a in place_obj.amenities] if hasattr(place_obj, "amenities") else []
        }

    def _review_to_dict(self, review_obj):
        if not review_obj:
            return None
        return {
            "id": review_obj.id,
            "text": review_obj.text,
            "rating": review_obj.rating,
            "user_id": review_obj.user.id,
            "place_id": review_obj.place.id
        }

    def create_user(self, user_data):
        existing = self.get_user_by_email(user_data["email"])
        if existing:
            raise ValueError("Cet email est déjà utilisé.")

        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"]
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def update_user(self, user_id, data):
        return self.user_repo.update(user_id, data)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    def create_amenity(self, amenity_data):
        name = amenity_data.get("name", "")
        if not name or len(name) > 50:
            raise ValueError("Invalid 'name': must be non-empty and ≤ 50 characters.")
        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)
        return self._amenity_to_dict(amenity)

    def get_amenity(self, amenity_id):
        return self._amenity_to_dict(self.amenity_repo.get(amenity_id))


    def get_all_amenities(self):
        return [self._amenity_to_dict(a) for a in self.amenity_repo.get_all()]

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        if "name" in amenity_data:
            if not amenity_data["name"] or len(amenity_data["name"]) > 50:
                raise ValueError("Invalid 'name': must be non-empty and ≤ 50 characters.")
        amenity.update(amenity_data)
        self.amenity_repo.add(amenity)
        return self._amenity_to_dict(amenity)

    def create_place(self, place_data):
        if place_data["price"] < 0:
            raise ValueError("Price must be a non-negative value.")
        if not (-90 <= place_data["latitude"] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= place_data["longitude"] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found.")
        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner
        )
        self.place_repo.add(place)
        return self._place_to_dict(place)

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        return self._place_to_dict(place)

    def get_all_places(self):
        return [self._place_to_dict(p) for p in self.place_repo.get_all()]

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        if "price" in place_data and place_data["price"] < 0:
            raise ValueError("Price must be a non-negative value.")
        if "latitude" in place_data and not (-90 <= place_data["latitude"] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if "longitude" in place_data and not (-180 <= place_data["longitude"] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        place.update(place_data)
        self.place_repo.add(place)
        return self._place_to_dict(place)

    def create_review(self, review_data):
        required_fields = ["text", "rating", "user_id", "place_id"]
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"Missing required field: {field}")
        if not (1 <= review_data["rating"] <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        user = self.user_repo.get(review_data["user_id"])
        if not user:
            raise ValueError("User not found.")
        place = self.place_repo.get(review_data["place_id"])
        if not place:
            raise ValueError("Place not found.")
        review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            user=user,
            place=place
        )
        self.review_repo.add(review)
        return self._review_to_dict(review)

    def get_review(self, review_id):
        return self._review_to_dict(self.review_repo.get(review_id))

    def get_all_reviews(self):
        return [self._review_to_dict(r) for r in self.review_repo.get_all()]

    def get_reviews_by_place(self, place_id):
        reviews = self.review_repo.get_all()
        filtered = [r for r in reviews if r.place.id == place_id]
        return [self._review_to_dict(r) for r in filtered]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        if "rating" in review_data:
            if not (1 <= review_data["rating"] <= 5):
                raise ValueError("Rating must be between 1 and 5.")
        review.update(review_data)
        self.review_repo.add(review)
        return self._review_to_dict(review)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return self._review_to_dict(review)
