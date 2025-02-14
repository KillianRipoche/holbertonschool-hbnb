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
