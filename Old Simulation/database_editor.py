import mysql.connector
from mysql.connector import Error
import hashlib


# Query Record:
# CREATE TABLE USERS (firstname CHAR(32) NULL, surname CHAR(32) NULL, username VARCHAR(32) NOT NULL,
# password VARCHAR(32) NOT NULL, PRIMARY KEY (username));
# Created user George


# To connect to MYSQL Server
def connect_to_server():
    first_connection = None
    try:
        first_connection = mysql.connector.connect(
            host="db4free.net",
            user="simdatabase",
            passwd="stokesfc2023",
            db="simulationdata"
        )
        print("Connected Successfully")
    except Error as error:
        print("Connection Unsuccessfully")
        print(f"Error: {error}")

    return first_connection


# Executes Queries on MYSQL server
def execute_query(connector, query):
    cursor = connector.cursor()
    try:
        cursor.execute(query)
        connector.commit()
        cursor.close()
        print("Executed Successfully")
    except Error as error:
        print("Executed Unsuccessfully")
        print(f"Error: {error}")


# Create a user record on MYSQL server
def create_user(connector, User, Pass, Name=None):
    cursor = connector.cursor()
    try:
        hashed_user = hashlib.md5((User + "ytrewq").encode()).hexdigest()
        hashed_pass = hashlib.md5((Pass + "qwerty").encode()).hexdigest()
        cursor.execute('SELECT * FROM USERS WHERE username = %s', (hashed_user,))
        already_exists = cursor.fetchall()
        if Name is not None:
            first_name = Name.split(" ")[0]
            surname = Name.split(" ")[1]
        else:
            first_name = "None"
            surname = "None"
        if len(already_exists) == 0:
            cursor.execute("insert into USERS(firstname, surname, username, password) values (%s, %s, %s, %s)",
                           (first_name, surname, hashed_user, hashed_pass))
            connector.commit()
            cursor.close()
            print("User Created Successfully")
        else:
            print("User Already Exists")
    except Error as error:
        print("Executed Unsuccessfully")
        print(f"Error: {error}")


# Search for users in USERS table on MYSQL server
def search_user(connector, entered_username, entered_password):
    cursor = connector.cursor()
    try:
        hashed_user = hashlib.md5((entered_username + "ytrewq").encode()).hexdigest()
        hashed_pass = hashlib.md5((entered_password + "qwerty").encode()).hexdigest()
        cursor.execute('SELECT * FROM USERS WHERE username = %s and password = %s', (hashed_user, hashed_pass))
        user_data = cursor.fetchall()
        print("Search Successful")
        if len(user_data) == 1:
            return True
        else:
            return False
    except Error as error:
        print("Search Unsuccessful")
        print(f"Error: {error}")


def select_users(connector):
    cursor = connector.cursor()
    try:
        cursor.execute('SELECT * FROM USERS')
        users = cursor.fetchall()
        print("Selection Successful")
        return users
    except Error as error:
        print("Selection Unsuccessful")
        print(f"Error: {error}")


def delete_user(connector, username, key):
    admin_key = "100604"
    cursor = connector.cursor()
    if key == admin_key:
        try:
            hashed_user = hashlib.md5((username + "ytrewq").encode()).hexdigest()
            before_deletion = select_users(connector)
            cursor.execute('delete from USERS where username = %s;', (hashed_user,))
            after_deletion = select_users(connector)
            connector.commit()
        except Error as error:
            print("Deletion Unsuccessful")
            print(f"Error: {error}")
            return error, False

        if len(before_deletion) == len(after_deletion):
            return "User Not Found", False
        else:
            return "Deletion Successful", True

    else:
        return "Admin Key Wrong", False


#

if __name__ == "__main__":
    connection = connect_to_server()
    print("Admin Key Wrong")
