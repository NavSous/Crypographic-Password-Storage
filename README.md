# Crypographic-Password-Storage
Storage of passwords in a SQLite database using cryptographic tools.

How to use this password storage system:

To create a new user object in the database, place the following code after the login function in the main python file: ```User(chosen_id, chosen_username, chosen_password)```

To log in to an account, enter its credentials when prompted. Once you are logged in you can enter a post to the database, which will be associated with your user account.
