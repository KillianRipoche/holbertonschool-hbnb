import re
from BaseModel import BaseModel
class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name[:50]  # Limite à 50 caractères
        self.last_name = last_name[:50]  # Limite à 50 caractères
        self.email = self.validate_email(email)  # Validation de l'email
        self.is_admin = is_admin
        self.places = []  # L'utilisateur peut posséder plusieurs places

    def validate_email(self, email):
        """Vérifie le format de l'email"""
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if re.match(email_regex, email):
            return email
        raise ValueError("Email invalide")

    def create_place(self, place):
        self.places.append(place)
        place.owner = self
