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
            raise ValueError(
                "Invalid 'title': must be non-empty and ≤ 100 characters.")

        if price < 0:
            raise ValueError("Invalid 'price': must be a positive number.")

        if not (-90 <= latitude <= 90):
            raise ValueError("Invalid 'latitude': must be between -90 and 90.")

        if not (-180 <= longitude <= 180):
            raise ValueError(
                "Invalid 'longitude': must be between -180 and 180.")

        from .user import User
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
