import hashlib as hlib
import binascii
import sqlite3
#Initialize SQLite client connected to a database
con = sqlite3.connect('main.db')
cur = con.cursor()
#Create a list of special characters for password security
special_characters = "!@#$%^&*()-+?_=,<>/'"
#Create salt to prevent rainbow table attacks
salt = "stoprainbowtables"

#Class for creating a user object (Create a user using: User(id, username, password))
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        #Ensure the password is safe (It is unsafe it is all one case or it lacks any special characters)
        if len(password) < 8 or not any(a in special_characters for a in password) or password.upper() == password or password.lower() == password:
            print("That password is not storng enough")
            return None
        #Salt the password and then hash it using sha256
        salted = password + salt
        pwd = hlib.sha256(salted.encode('utf8')).hexdigest()
        #Prevent multiple of the same usernames or id's being in the database
        x = None
        y = None
        for row in cur.execute('''SELECT * FROM users WHERE username = ?''', (self.username,)):
            x = row
        for row in cur.execute('''SELECT * FROM users WHERE id = ?''', (self.id,)):
            x = row
        if x!=None:
            print("That username or ID is already in use")
        else:
            #Insert data into the SQLite database
            cur.execute("INSERT INTO users (id, username, password) VALUES (?, ?, ?)", (self.id, self.username, pwd))
            con.commit()

#Function for authenticating the user
def login(uname, pword):
    x = None
    #Use the uname parameter to search for the object from the database with the same username
    for row in cur.execute('''SELECT * FROM users WHERE username = ?''', (uname,)):
        x = row
    #If no user object is found with that username, return a failed authentication
    if x == None:
        return False, None
    Auth = False
    AuthId = None
    #Hash and salt the password that the user entered through the pword parameter
    hash_psw = psword + salt
    hash_psw = hlib.sha256(hash_psw.encode('utf8')).hexdigest()
    #If the hashed password matches the one in the database, return a successfull authentication with the id of the account that was logged in to
    if hash_psw == x[2]:
        Auth = True
        AuthId = x[0]
    if Auth:
        print("You have been successfully authenticated")
    return Auth, AuthId

#Promt the user to enter their information
usrname = input("Enter you username: ")
psword = input("Enter you password: ")
#auth_result is the tuple that stores the output of the login function. It has two elements: if the user logged in successfully and if so the id of the account they logged in to
auth_result = login(usrname, psword)
#If the authentication succeeded
if auth_result[0]:
    #Find the user object by the id
    for row in cur.execute('''SELECT * FROM users WHERE id = ?''', (auth_result[1],)):
        x = row
    #Print a success statement
    print("You are know logged in to the account with these properties: ", x)
    #Allow the user to create a post to the database
    ip = input("Enter what you want your post to be: ")
    cur.execute("INSERT INTO posts (user_id, user_username, comment_text) VALUES (?, ?, ?)", (x[0], x[1], ip))
    con.commit()
#If the authentication failed
else:
    print("Incorrect username or password")
con.close()     