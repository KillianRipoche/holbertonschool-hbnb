from app.persistence.repository import InMemoryRepository
from models.user import User
import uuid

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def create_amenity(self, amenity_data):
        amenity = amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            self.amenity_repo.update(amenity)
            return amenity

    def create_place(self, place_data):
        if place_data['price'] < 0:
            raise ValueError("Price must be a non-negative value.")
        if not (-90 <= place_data['latitude'] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= place_data['longitude'] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        place = self.place_repo.create(place_data)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise ValueError("Place not found.")

        owner = self.user_repo.get_by_id(place.owner_id)
        amenities = self.amenity_repo.get_by_ids(place.amenities)

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            },
            'amenities': [{'id': amenity.id, 'name': amenity.name}
                          for amenity in amenities]
        }

    def get_all_places(self):
        places = self.place_repo.get_all()
        return [{
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude
        } for place in places]

    def update_place(self, place_id, place_data):
        if place_data.get('price') and place_data['price'] < 0:
            raise ValueError("Price must be a non-negative value.")
        if place_data.get('latitude') and not(-90 <= place_data['latitude'] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if place_data.get('longitude') and not(-180 <= place_data['longitude'] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        place = self.place_repo.update(place_id, place_data)
        return place

    def create_review(self, review_data):
        required_fields = ['text', 'rating', 'user_id', 'place_id']
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"Missing required field: {field}")

        if not (1 <= review_data['rating'] <= 5):
            raise ValueError(f"Missing required field: {field}")

        if not self.user_repo.get(review_data['user_id']):
            raise ValueError("User not found.")

        if not self.place_repo.get(review_data['place_id']):
            raise ValueError("Place not found.")

        review_id = str(uuid.uuid4())
        review_data['id'] = review_id
        self.review_repo.add(review_data)
        return review_data

    def get_review(self, review_id):
        # Retrieve a review by id
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # Retrieve all reviews for a specific place
        reviews = self.review_repo.get_all()
        return [review for review in reviews if review.get('place_id') == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Update text if provided
        if 'text' in review_data:
            review['text'] = review_data['text']

        # Update rating if provided with validation
        if 'rating' in review_data:
            if not (1 <= review_data['rating'] <= 5):
                raise ValueError("Rating must be between 1 and 5.")
            review['rating'] = review_data['rating']

        self.review_repo.update(review)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return review
