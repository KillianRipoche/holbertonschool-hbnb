import uuid
from datetime import datetime

class BaseModel:
    """"""

    def __init__(self):
        self.id = str(uuid.uuid4())       # Génère un UUID unique
        self.created_at = datetime.now()  # Date de création
        self.updated_at = datetime.now()  # Date de dernière mise à jour

    def save(self):
        """"""
        self.updated_at = datetime.now()
