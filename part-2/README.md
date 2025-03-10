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
