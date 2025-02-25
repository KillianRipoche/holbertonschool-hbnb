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
