import re
from .BaseModel import BaseModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


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

    def __init__(self, first_name, last_name, email, password, is_admin=False):
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

        # Validate password
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValueError(
                "Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValueError(
                "Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r'[\W_]', password):
            raise ValueError(
                "Password must contain at least one special character.")

        self.hash_password(password)
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

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
