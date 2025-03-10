import re
from .BaseModel import BaseModel


class User(BaseModel):
    """
    User class.
    Attributes:
      - id (from BaseModel)
      - first_name, last_name: Required, max 50 characters
      - email: Required, must be unique, must follow email format
      - is_admin: Boolean (default: False)
      - places: List of owned Places
      - reviews: List of written Reviews

    Validation:
      - first_name and last_name must not be empty and <= 50 characters
      - email format must be valid and unique
    """

    existing_emails = set()

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        # Validate first_name
        if not first_name or len(first_name) > 50:
            raise ValueError("first_name invalide (not empty, max 50).")

        # Validate last_name
        if not last_name or len(last_name) > 50:
            raise ValueError("last_name invalide (not empty, max 50).")

        # Validate email (format + uniqueness)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")
        if email in User.existing_emails:
            raise ValueError("This email is already in use.")
        User.existing_emails.add(email)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        # Relations
        self.places = []   # Lieux possédés par l'utilisateur
        self.reviews = []  # Avis rédigés

    def add_place(self, place):
        """Adds a Place to the user's list of owned places."""
        from .place import Place
        if not isinstance(place, Place):
            raise TypeError("Expected 'place' to be an instance of Place.")
        self.places.append(place)

    def add_review(self, review):
        """Adds a Review to the user's list of written reviews."""
        from .review import Review
        if not isinstance(review, Review):
            raise TypeError("Expected 'review' to be an instance of Review.")
        self.reviews.append(review)
