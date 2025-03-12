# HBnB Project: Part 2 - Implementation of Business Logic and API Endpoints

## Overview
In Part 2 of the HBnB Project, we focus on implementing the core business logic and API endpoints using Python and Flask. This phase is dedicated to building the Presentation and Business Logic layers, implementing the necessary classes, and defining the API endpoints required for user interactions.

The goal is to create a functional and scalable API that allows managing Users, Places, Reviews, and Amenities while adhering to best practices in RESTful API design. The Persistence layer will be introduced in Part 3, so for now, an in-memory repository will be used for data storage.

## Project Structure
The project is organized into the following layers:

- **Presentation Layer:** Defines the API endpoints using Flask and flask-restx.
- **Business Logic Layer:** Implements the core application logic, including validation, relationships, and data manipulation.
- **Persistence Layer:** Currently uses an in-memory repository but will be replaced with a database-backed solution in Part 3.

## Objectives
### 1. Project Setup and Structure
- Organize the project into a modular architecture.
- Prepare the application for integrating the Facade pattern.
- Implement an in-memory repository for temporary data storage.

### 2. Business Logic Implementation
- Develop core business logic classes: `User`, `Place`, `Review`, `Amenity`.
- Define relationships between entities.
- Ensure proper validation and data integrity handling.

### 3. RESTful API Endpoints
- Implement API endpoints for managing:
  - **Users**: Create, retrieve, update (no delete).
  - **Amenities**: Create, retrieve, update (no delete).
  - **Places**: Create, retrieve, update (no delete).
  - **Reviews**: Create, retrieve, update, delete.
- Use flask-restx to define and document APIs.
- Ensure data serialization returns extended attributes where applicable.

### 4. Testing and Validation
- Perform unit tests on business logic and API endpoints.
- Test using Postman, cURL, and automated test scripts.
- Validate API responses and ensure proper error handling.

## API Endpoints
### User Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/v1/users/` | Create a new user |
| GET | `/api/v1/users/` | Retrieve all users |
| GET | `/api/v1/users/<user_id>` | Retrieve a specific user |
| PUT | `/api/v1/users/<user_id>` | Update user details |

### Amenity Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/v1/amenities/` | Create a new amenity |
| GET | `/api/v1/amenities/` | Retrieve all amenities |
| GET | `/api/v1/amenities/<amenity_id>` | Retrieve a specific amenity |
| PUT | `/api/v1/amenities/<amenity_id>` | Update amenity details |

### Place Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/v1/places/` | Create a new place |
| GET | `/api/v1/places/` | Retrieve all places |
| GET | `/api/v1/places/<place_id>` | Retrieve a specific place |
| PUT | `/api/v1/places/<place_id>` | Update place details |

### Review Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/v1/reviews/` | Create a new review |
| GET | `/api/v1/reviews/` | Retrieve all reviews |
| GET | `/api/v1/reviews/<review_id>` | Retrieve a specific review |
| PUT | `/api/v1/reviews/<review_id>` | Update review details |
| DELETE | `/api/v1/reviews/<review_id>` | Delete a review |

## Testing
To ensure the API functions as expected:
1. Use **pytest** and Flask’s test client to run unit tests.
2. Manually test endpoints using **Postman** or **cURL**.
3. Validate API documentation with **Swagger UI** (flask-restx provides automatic API documentation).

**Main file for testing**
```
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

def main():
    # Création d'un utilisateur
    user1 = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    user2 = User(first_name="Bob", last_name="Johnson", email="bob@example.com")

    # Création de lieux
    place1 = Place(
        title="Appartement Cozy",
        description="Superbe appartement en centre-ville",
        price=100.0,
        latitude=48.8566,
        longitude=2.3522,
        owner=user1
    )
    place2 = Place(
        title="Villa Luxueuse",
        description="Villa avec piscine",
        price=300.0,
        latitude=43.2965,
        longitude=5.3698,
        owner=user2
    )

    # L'utilisateur 1 possède place1
    user1.add_place(place1)
    # L'utilisateur 2 possède place2
    user2.add_place(place2)

    # Création d'équipements
    wifi = Amenity(name="Wi-Fi")
    parking = Amenity(name="Parking")

    # Ajout des équipements
    place1.add_amenity(wifi)
    place1.add_amenity(parking)
    place2.add_amenity(wifi)

    # Création d'un avis (Review)
    review1 = Review(text="Super séjour !", rating=5, place=place1, user=user2)
    review2 = Review(text="Pas mal du tout", rating=4, place=place2, user=user1)

    # Ajout de l'avis à la fois au lieu et à l'utilisateur
    place1.add_review(review1)
    user2.add_review(review1)

    place2.add_review(review2)
    user1.add_review(review2)

    # Affichage des résultats
    print(f"Le lieu '{place1.title}' a {len(place1.reviews)} avis.")
    print(f"L'utilisateur {user2.first_name} a écrit {len(user2.reviews)} avis.")
    print(f"L'utilisateur {user1.first_name} possède {len(user1.places)} lieux.")
    print(f"Le lieu '{place1.title}' a {len(place1.amenities)} équipements.")

    print(f"Le lieu '{place2.title}' a {len(place2.reviews)} avis.")
    print(f"L'utilisateur {user1.first_name} a écrit {len(user1.reviews)} avis.")

if __name__ == "__main__":
    main()
```

## Technologies Used
- **Python** (Flask, flask-restx)
- **pytest** (for unit testing)
- **Postman/cURL** (for API testing)
- **RESTful API design principles**

## Future Enhancements
- **Implement JWT authentication** and role-based access control in Part 3.
- **Migrate to a database-backed persistence layer** using SQLAlchemy.
- **Enhance error handling** and implement rate-limiting for API security.

## Resources
- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [flask-restx Documentation](https://flask-restx.readthedocs.io/en/latest/)
- [RESTful API Design Best Practices](https://restfulapi.net/)

---
##### CONTRIBUTORS :

**Jean-Alain Renié** : https://github.com/JaRenie-spec

**Killian Ripoche** : https://github.com/KillianRipoche

**Alexis Battistoni** : https://github.com/Albat93
