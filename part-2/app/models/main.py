from user import User
from place import Place
from review import Review
from amenity import Amenity

def main():
    # Création des utilisateurs
    user1 = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    user2 = User(first_name="Bob", last_name="Johnson", email="bob@example.com")

    # Création de lieux
    place1 = Place(title="Appartement Cozy", description="Superbe appartement en centre-ville", price=100, latitude=48.8566, longitude=2.3522, owner=user1)
    place2 = Place(title="Villa Luxueuse", description="Villa avec piscine", price=300, latitude=43.2965, longitude=5.3698, owner=user2)

    # Ajout des lieux à leurs propriétaires
    user1.add_place(place1)
    user2.add_place(place2)

    # Création d'équipements
    wifi = Amenity(name="Wi-Fi")
    parking = Amenity(name="Parking")

    # Ajout des équipements aux lieux
    place1.add_amenity(wifi)
    place1.add_amenity(parking)
    place2.add_amenity(wifi)

    # Création d'un avis
    review1 = Review(text="Super séjour !", rating=5, place=place1, user=user2)

    # Ajout de l'avis au lieu et à l'utilisateur
    place1.add_review(review1)
    user2.add_review(review1)

    # Affichage des résultats
    print(f"Le lieu '{place1.title}' a {len(place1.reviews)} avis.")
    print(f"L'utilisateur {user2.first_name} a écrit {len(user2.reviews)} avis.")
    print(f"L'utilisateur {user1.first_name} possède {len(user1.places)} lieux.")
    print(f"Le lieu '{place1.title}' a {len(place1.amenities)} équipements.")

if __name__ == "__main__":
    main()
