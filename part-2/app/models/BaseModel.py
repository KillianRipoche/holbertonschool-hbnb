import uuid
from datetime import datetime

class BaseModel:
    """
    Base class that provides:
      - Unique ID (UUID)
      - Timestamps (created_at, updated_at)
      - Methods to update attributes and timestamps
    """
    def __init__(self):
        self.id = str(uuid.uuid4())       # Génère un UUID unique
        self.created_at = datetime.now()  # Date de création
        self.updated_at = datetime.now()  # Date de dernière mise à jour

    def save(self):
        """Update the 'updated_at' timestamp when the object is modified."""
        self.updated_at = datetime.now()

    def update(self, data: dict):
        """
        Update object attributes from a dictionary.
        Also updates the 'updated_at' timestamp.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
