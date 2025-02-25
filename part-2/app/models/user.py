import re
<<<<<<< HEAD
from BaseModel import BaseModel
from place import Place
from review import Review
class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name[:50]  # Limite à 50 caractères
        self.last_name = last_name[:50]  # Limite à 50 caractères
        self.email = self.validate_email(email)  # Validation de l'email
        self.is_admin = is_admin
        self.places = []  # L'utilisateur peut posséder plusieurs places
        self.reviews = []

    def validate_email(self, email):
        """Vérifie le format de l'email"""
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if re.match(email_regex, email):
            return email
        raise ValueError("Email invalide")

    def add_place(self, place):
        if isinstance(place, Place):
            self.places.append(place)
            place.owner = self

    def add_review(self, review):
        if isinstance(review, Review):
            self.reviews.append(review)
=======
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
            raise ValueError("first_name invalide (non vide, max 50).")

        # Validate last_name
        if not last_name or len(last_name) > 50:
            raise ValueError("last_name invalide (non vide, max 50).")

        # Validate email (format + uniqueness)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Format d'email invalide.")
        if email in User.existing_emails:
            raise ValueError("Cet email est déjà utilisé.")
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
>>>>>>> origin/Killian
