from BaseModel import BaseModel
from place import Place

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name[:50]  # Limité à 50 caractères
        self.places = []  # Liste des endroits où cet équipement est disponible
        self.amenities = []

    def associate_with_place(self, place):
        if place not in self.places:
            self.places.append(Place)
            self.amenities.append(Place)
