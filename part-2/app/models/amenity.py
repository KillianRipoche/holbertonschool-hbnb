<<<<<<< HEAD
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
=======
from .BaseModel import BaseModel

class Amenity(BaseModel):
    """
    Amenity class.
    Attributes:
      - id (from BaseModel)
      - name: Required, max 50 characters
      - created_at (from BaseModel)
      - updated_at (from BaseModel)

    Validation:
      - name must be non-empty and ≤ 50 characters
    """

    def __init__(self, name):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("Invalid 'name': must be non-empty and ≤ 50 characters.")
        self.name = name
>>>>>>> origin/Killian
