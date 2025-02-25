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
