# HBnB Class Diagram Documentation

## 1. Class Diagram Overview

```mermaid
classDiagram
direction TB

class BaseModel{
-id : str
+created at : time
+updated at : time
}
class User{
+First name
-Last name
-Email
#user.id
#Password
~def create_user()
#def change_permission()
~def del_user()
~def modify_user()
+def list_user_place()
}
class Place{
+Title
+Description
+Price
+Location : Latitude / longitude
+Owner = user.id
~def create_place()
~def modify_place()
~def del_place()
}
class Amenity{
+Name
+Description
~def create_amenity()
~def modify_amenity()
~def del_amenity()
~def list_amenity()
}
class Review{
+Place
+User
+Rating
+Comment
#user.id
~def create_review()
~def modify_review()
~def del_review()
~def list_by_place()
}

BaseModel --|> User : Inheritance
BaseModel --|> Place : Inheritance
BaseModel --|> Amenity : Inheritance
BaseModel --|> Review : Inheritance

Place "1" <.. "0..*" Amenity : Dependency

Place "1" <--> "0..*" Review : Association
User "1" <--> "0..*" Review : Association
User "1" <--> "0..*" Place : Association

style BaseModel fill:#d3d3d3,stroke:#000,stroke-width:2px;
style User fill:#ADD8E6,stroke:#000,stroke-width:2px;
style Place fill:#90EE90,stroke:#000,stroke-width:2px;
style Amenity fill:#FFA500,stroke:#000,stroke-width:2px;
style Review fill:#FF6347,stroke:#000,stroke-width:2px;

### Description
The Class Diagram provides a structured representation of the system’s data model, illustrating how different entities interact within the application.

### Main Classes and Relationships
- **BaseModel**: A parent class that provides common attributes (ID, timestamps) for all entities.
- **User**: Represents registered users with authentication and management functionalities.
- **Place**: Stores property details such as location, price, and owner.
- **Amenity**: Represents features available at a property.
- **Review**: Allows users to rate and comment on places.

### Design Decisions
- **Inheritance**: The BaseModel class ensures consistency across all entities.
- **Associations**: User, Place, and Review classes maintain clear relationships to support data integrity.

---

## 3. Detailed Explanation of Classes

### BaseModel
- **Description**:
  - The superclass that provides common fields (id, created_at, updated_at) to all entities.
  - Ensures uniformity and reusability across different data models.

### User
- **Attributes**:
  - first_name, last_name, email, password, user.id
- **Methods**:
  - `create_user()`: Registers a new user.
  - `change_permission()`: Modifies user roles.
  - `del_user()`, `modify_user()`: Manage user profiles.
  - `list_user_place()`: Retrieves places owned by the user.
- **Relationships**:
  - Can create Places (One-to-Many relationship).
  - Can submit Reviews (One-to-Many relationship).

### Place
- **Attributes**:
  - title, description, price, latitude, longitude, owner = user.id
- **Methods**:
  - `create_place()`, `modify_place()`, `del_place()`: CRUD operations for places.
- **Relationships**:
  - Owned by a User.
  - Can have multiple Amenities (Many-to-Many relationship).
  - Can receive multiple Reviews (One-to-Many relationship).

### Amenity
- **Attributes**:
  - name, description
- **Methods**:
  - `create_amenity()`, `modify_amenity()`, `del_amenity()`: CRUD operations for amenities.
- **Relationships**:
  - Linked to Places through a Many-to-Many relationship.

### Review
- **Attributes**:
  - place, user, rating, comment, user.id
- **Methods**:
  - `create_review()`, `modify_review()`, `del_review()`: CRUD operations for reviews.
- **Relationships**:
  - Associated with a User (Many-to-One relationship).
  - Associated with a Place (Many-to-One relationship).

---

## 4. Class Diagram Structure and Integrity

- The inheritance structure ensures all classes share common properties via BaseModel.
- One-to-Many and Many-to-Many relationships ensure logical data storage and retrieval.
- Encapsulation and abstraction principles are applied to keep operations modular and maintainable.

---

## 5. Conclusion
This document provides a detailed analysis of the HBnB Class Diagram, explaining the relationships and functionalities of each entity. Understanding these components ensures a clear and scalable implementation of the system’s business logic.
