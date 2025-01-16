# Marriage Matchmaking App

## Brief Description
The Marriage Matchmaking App is a simple backend application designed to help users find potential matches based on their profile information. The app allows users to create, read, update, and delete profiles with details such as name, age, gender, email, city, and interests.


### Functionality:

- Create User Endpoint: Create a new user profile.
- Read Users Endpoint: Retrieve a list of user profiles.
- Read User by ID Endpoint: Retrieve a user profile by ID.
- SQLite Database: The application uses SQLite as the database to store user profiles.


### Tasks:
1. Add User Update Endpoint:
   - Implement an endpoint to update user details by ID in the main.py file.
2. Add User Deletion Endpoint:
   - Implement an endpoint to delete a user profile by ID.
3. Find Matches for a User:
   - Implement an endpoint to find potential matches for a user based on their profile information.
4. Add Email Validation:
   - Add validation to ensure the email field in user profiles contains valid email addresses.


### My Approach

#### Preface 

To be perfectly candid, I haven't worked much on FastAPI and had to learn it while doing this project from the code and context clues.

#### Environment
Python - 3.12.4

#### Preliminary changes
1. Implemented a simple '/hello' route for server check

2. Changed the way interests are stored from `ARRAY` to String - using ARRAY returned `ARRAY` not supported by SQLite error.

    -Converted List of interests to JSON and string and stored JSON string. 
    
    -Implemented methods, `get_interests` and `set_interests` to handle the columnn interests

3. Implemented a `get_user()` function to parse SQLite model object to a Dictionary

4. Updated deprecated methods and attributes to latest ones.


#### Task-1 User Data Update
1. The UserUpdate schema is used to accept the updated user information.
2. The endpoint retrieves the user from the database by their ID, updates the user fields with the new data if provided, and commits the changes.
3. Added validation to ensure the user exists, returning a 404 status code if the user is not found.

#### Task-2: User Deletion
1. The DELETE endpoint is created to delete a user profile.
2. It first checks if the user exists. If the user is found, the profile is deleted, and the database is committed. If the user is not found, it returns a 404 status code.


#### Task-3: Find Matches for a User

1. The matches endpoint takes a user ID and returns other users who share common interests and have a similar age 
2. Matching users are returned as a list of user profiles.
3. Extra Filters can be added through query params for city-based filtering etc

#### Task-4: Add Email Validation
1. The EmailStr type from Pydantic is used to validate email addresses.
2. When a user profile is created or updated, Pydantic ensures that the email is in a valid format.
3. If the email is invalid, FastAPI automatically returns a 422 Unprocessable Entity error.
