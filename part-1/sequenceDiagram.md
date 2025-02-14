```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

box Login Process
	User ->> API: Enter credentials
	API ->> BusinessLogic: Verify password
	BusinessLogic ->> Database: Query user data
	Database -->> BusinessLogic: Return user data
	alt If password is valid
		BusinessLogic -->> API: return OK
		API -->> User: return JWT (success)
	else If password is invalid
		BusinessLogic -->> API: return Invalid
		API -->> User: failed login
	end
end
```
