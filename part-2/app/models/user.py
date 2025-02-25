from BaseModel import BaseModel
from place import Place
from review import Review


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # Places list
        self.reviews = []  # Reviews list

    def add_place(self, place):
        """"""
        if isinstance(place, Place):
            self.places.append(place)

    def add_review(self, review):
        """"""
        if isinstance(review, Review):
            self.reviews.append(review)
