from app import db
from app.models.BaseModel import BaseModel


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
