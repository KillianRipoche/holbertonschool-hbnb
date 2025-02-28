import unittest
import uuid
from datetime import datetime
from app.models.BaseModel import BaseModel  # Assurez-vous que BaseModel est correctement importé
import time

class TestBaseModel(unittest.TestCase):

    def test_instance_creation(self):
        """Teste la création d'une instance de BaseModel."""
        obj = BaseModel()
        self.assertIsInstance(obj, BaseModel)
        self.assertIsInstance(obj.id, str)
        self.assertIsInstance(uuid.UUID(obj.id), uuid.UUID)  # Vérifie si l'ID est un UUID valide
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)

    def test_unique_id(self):
        """Vérifie que chaque instance a un ID unique."""
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.assertNotEqual(obj1.id, obj2.id)

    def test_save_updates_timestamp(self):
        """Vérifie que `save()` met à jour `updated_at`."""
        obj = BaseModel()
        old_updated_at = obj.updated_at
        time.sleep(1)  # Pause pour s'assurer du changement de timestamp
        obj.save()
        self.assertGreater(obj.updated_at, old_updated_at)

    def test_update_method(self):
        """Teste la méthode update() pour modifier les attributs."""
        obj = BaseModel()
        old_updated_at = obj.updated_at
        obj.update({"id": "test-id", "created_at": obj.created_at, "new_attr": "test"})

        # Vérification des mises à jour
        self.assertEqual(obj.id, "test-id")  # L'ID doit être mis à jour
        self.assertFalse(hasattr(obj, "new_attr"))  # Ne doit pas ajouter de nouveaux attributs
        self.assertGreater(obj.updated_at, old_updated_at)  # `updated_at` doit être mis à jour

if __name__ == '__main__':
    unittest.main()
