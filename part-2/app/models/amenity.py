from BaseModel import BaseModel
class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name[:50]  # Limité à 50 caractères
        self.places = []  # Liste des endroits où cet équipement est disponible
