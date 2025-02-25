<<<<<<< HEAD
from BaseModel import BaseModel
class Review(BaseModel):
    def __init__(self, content, rating, user, place):
        super().__init__()
        self.content = content
        self.rating = self.validate_rating(rating)  # Vérification de la note
        self.user = user  # L'utilisateur qui a écrit l'avis
        self.place = place  # La place qui est évaluée

    def validate_rating(self, rating):
        """Vérifie que la note est entre 1 et 5"""
        if not (1 <= rating <= 5):
            raise ValueError("La note doit être entre 1 et 5.")
        return rating

    def update_content(self, new_content):
        self.content = new_content
        self.save()
=======
from .BaseModel import BaseModel

class Review(BaseModel):
    """
    Review class.
    Attributes:
      - id (from BaseModel)
      - text: Required (content of the review)
      - rating: Integer, must be between 1 and 5
      - place: Place being reviewed
      - user: User who wrote the review
      - created_at (from BaseModel)
      - updated_at (from BaseModel)

    Validation:
      - text must not be empty
      - rating must be between 1 and 5
    """

    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text:
            raise ValueError("Invalid 'text': review content must not be empty.")
        if not (1 <= rating <= 5):
            raise ValueError("Invalid 'rating': must be between 1 and 5.")

        from .place import Place
        if not isinstance(place, Place):
            raise TypeError("Invalid 'place': must be an instance of Place.")

        from .user import User
        if not isinstance(user, User):
            raise TypeError("Invalid 'user': must be an instance of User.")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
>>>>>>> origin/Killian
