# Introduction

The purpose of this document is to provide a comprehensive preview guide for the implementation of the HBnB project. HBnB is a platform designed to facilitate the connection between hosts offering accommodations and travelers seeking short-term rentals, similar to established services like Airbnb. The platform allows hosts to list their properties, manage bookings, and communicate with guests, while providing a seamless and secure booking experience for users.

This preview document serves as a blueprint for the development and deployment of the HBnB system. It outlines the core architecture, features, and functionality of the platform, providing detailed insights into the technical requirements, system components, and integration processes. The document is intended for developers, system architects, and project managers, guiding them through the implementation process by offering clear, structured instructions on building and scaling the platform efficiently. By following this guide, the team can ensure a successful, streamlined development of the HBnB project, meeting the outlined goals and delivering a reliable and user-friendly solution.

# Infrastucture Preview

## Package Diagram

![Package Diagram](https://github.com/Albat93/holbertonschool-hbnb/blob/20bf0b2814eb10a6d335c625eecf364cc6d2e691/part-1/package_diagram.png)

## Class Diagram

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
```

## Sequence Diagram

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database


%% User registration :

User->>API: Register (User Data)
API->>BusinessLogic: Validate and Process Request
BusinessLogic->>Database: Check if user exists
Database-->>BusinessLogic: User not found (Success)
BusinessLogic->>Database: Save new user
Database-->>BusinessLogic: Confirm Save
BusinessLogic-->>API: Return Success
API-->>User: Registration Successful
Database-->>BusinessLogic: User found (Failed)
BusinessLogic-->>API: Return Failed
API-->>User: Registration Failed


%% Place registration :

User->>API: POST /places (Place Data)
API->>BusinessLogic: Validate and Process Request
BusinessLogic->>Database: Verify User Authentication
Database-->>BusinessLogic: Authentication Valid
BusinessLogic->>Database: Save Place Data
Database-->>BusinessLogic: Confirm Save
BusinessLogic-->>API: Return Place Created Response
API-->>User: Place Created Successfully
Database-->>BusinessLogic: Authentication Failed or place conflit
BusinessLogic-->>API: Return conflit or authentication failed Response
API-->>User: Creation Failed


%% Review submission :

User->>API: POST /reviews (Review Data)
API->>BusinessLogic: Validate and Process Request
BusinessLogic->>Database: Check User and Place Existence
Database-->>BusinessLogic: Validation Success
BusinessLogic->>Database: Save Review Data
Database-->>BusinessLogic: Confirm Save
BusinessLogic-->>API: Return Review Created Response
API-->>User: Review Submitted Successfully
Database-->>BusinessLogic: Validation Failed
BusinessLogic-->>API: Return Review Failed
API-->>User: Review Submitted Failed


%% Fetching list of place :

User->>API: GET /places criteria
API->>BusinessLogic: Process Search Criteria
BusinessLogic->>Database: Retrieve Matching Places
Database-->>BusinessLogic: Return Places Data
BusinessLogic-->>API: Format and Return Response
API-->>User: List of Places
Database-->>BusinessLogic: Return Failed
BusinessLogic-->>API: Return failed
API-->>User: No matching place
```
## Authors:

**Alexis Battistoni** https://github.com/Albat93

**Killian Ripoche** https://github.com/KillianRipoche

**Jean-Alain Renié** https://github.com/JaRenie-spec
