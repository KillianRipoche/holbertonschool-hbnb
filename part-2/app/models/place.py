from BaseModel import BaseModel
from amenity import Amenity
from review import Review


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # Un objet User
        self.reviews = []  # Liste des avis associés
        self.amenities = []  # Liste des équipements associés

    def add_review(self, review):
        """"""
        if isinstance(review, Review):
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """"""
        if isinstance(amenity, Amenity) and amenity not in self.amenities:
            self.amenities.append(amenity)
