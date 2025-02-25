<<<<<<< HEAD
from BaseModel import BaseModel
class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title[:100]  # Limite à 100 caractères
        self.description = description
        self.price = self.validate_price(price)  # Vérification du prix
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = owner  # L'owner doit être un utilisateur existant
        self.reviews = []  # Liste des avis sur cet endroit
        self.amenities = []  # Liste des équipements

    def validate_price(self, price):
        """Vérifie que le prix est positif"""
        if price <= 0:
            raise ValueError("Le prix doit être positif.")
        return price

    def validate_latitude(self, latitude):
        """Vérifie que la latitude est dans la plage valide"""
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude doit être entre -90 et 90.")
        return latitude

    def validate_longitude(self, longitude):
        """Vérifie que la longitude est dans la plage valide"""
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude doit être entre -180 et 180.")
        return longitude

    def add_review(self, review):
        from .review import Review

        if not isinstance(review, Review):
            raise TypeError ("must be instance of review")
        self.reviews.append(review)
        review.place = self

    def add_amenity(self, amenity):
        from .amenity import Amenity

        if not isinstance(amenity, Amenity):
            raise TypeError ("must be instance of amenity")
        self.amenities.append(amenity)
        amenity.places.append(self)  # Ajouter cette place à l'amenity
=======
from .BaseModel import BaseModel

class Place(BaseModel):
    """
    Place class.
    Attributes:
      - id (from BaseModel)
      - title: Required, max 100 characters
      - description: Optional
      - price: Float, must be positive
      - latitude: Must be between -90 and 90
      - longitude: Must be between -180 and 180
      - owner: User who owns the place
      - reviews: List of associated reviews
      - amenities: List of associated amenities

    Validation:
      - title must be non-empty and ≤ 100 characters
      - price must be >= 0
      - latitude must be in range [-90, 90]
      - longitude must be in range [-180, 180]
    """

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError("Invalid 'title': must be non-empty and ≤ 100 characters.")

        if price < 0:
            raise ValueError("Invalid 'price': must be a positive number.")

        if not (-90 <= latitude <= 90):
            raise ValueError("Invalid 'latitude': must be between -90 and 90.")

        if not (-180 <= longitude <= 180):
            raise ValueError("Invalid 'longitude': must be between -180 and 180.")

        from .user import User  # Import différé
        if not isinstance(owner, User):
            raise TypeError("Expected 'owner' to be an instance of User.")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Adds a Review to the Place."""
        from .review import Review
        if not isinstance(review, Review):
            raise TypeError("Expected 'review' to be an instance of Review.")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Adds an Amenity to the Place."""
        from .amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise TypeError("Expected 'amenity' to be an instance of Amenity.")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
>>>>>>> origin/Killian
