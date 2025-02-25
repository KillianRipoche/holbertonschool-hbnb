from BaseModel import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        if 1 <= rating <= 5:
            self.text = text
            self.rating = rating
            self.place = place
            self.user = user
        else:
            raise ValueError("La note doit être comprise entre 1 et 5")
