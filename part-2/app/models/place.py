from BaseModel import BaseModel
class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title[:100]  # Limite à 100 caractères
        self.description = description
        self.price = self.validate_price(price)  # Vérification du prix
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = owner  # L'owner doit être un utilisateur existant
        self.reviews = []  # Liste des avis sur cet endroit
        self.amenities = []  # Liste des équipements

    def validate_price(self, price):
        """Vérifie que le prix est positif"""
        if price <= 0:
            raise ValueError("Le prix doit être positif.")
        return price

    def validate_latitude(self, latitude):
        """Vérifie que la latitude est dans la plage valide"""
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude doit être entre -90 et 90.")
        return latitude

    def validate_longitude(self, longitude):
        """Vérifie que la longitude est dans la plage valide"""
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude doit être entre -180 et 180.")
        return longitude

    def add_review(self, review):
        self.reviews.append(review)
        review.place = self

    def add_amenity(self, amenity):
        self.amenities.append(amenity)
        amenity.places.append(self)  # Ajouter cette place à l'amenity
