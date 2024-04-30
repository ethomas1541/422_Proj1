# Authors: Brian Griffith, Elijah Thomas, Drew Tweedale
# Last Modified: April 29 2024
# Group 5

# This module establishes connection with the note storage system and stores the users notes within 
# their associated table in the system.

import mysql.connector
from mysql.connector import Error
import sample_note


error_flag = False #variable for tracking errors

#Makes a new database if there is no database
def create_database_if_not_exists(connection, database_name):
    """
        Args:
            connection:
                Object used for accessing the server

            database_name:
                Name of the datbase you are checking for the existence of

        This function checks for if the database exists and creates one if it doesn't 
    """

    cursor = connection.cursor() #variable for iterating through the database
    cursor.execute(f"SHOW DATABASES LIKE '{database_name}'") #checks if a database with database name exists
    result = cursor.fetchone() #checks if theres anything in the database
    if not result:
        try:
            #if the result is empty it means there wasn't a preexisting database and so it creates one
            cursor.execute(f"CREATE DATABASE {database_name}")
            print(f"Database '{database_name}' created successfully.")
        except Error as err:
            #Code for catching potential errors
            print(f"Failed to create database '{database_name}': {err}")
    cursor.close()

#Connects to the server
def connect_to_mysql(host, port, user, password):
    """
        host:
            Name of the host you are connecting to
        port:
            The port number that the host is listening on
        user:
            Name of the user
        password:
            Password associated with the user

        Returns:
            Object for interacting with the server or none if no connection is established

        Establishes the initial connection to the server    
    """

    try:
        #Establishes a connection to the server and returns an object that allows access to the server
        return mysql.connector.connect(host=host, port=port, user=user, password=password)
    except Error as err:
        #Code for catching a failed connection
        print(f"Error connecting to MySQL Server: {err}")
        global error_flag
        error_flag = True
        return None

#Connects to the database
def connect_to_database(host, port, user, password, database):
    """
        host:
            Name of the host you are connecting to
        port:
            The port number that the host is listening on
        user:
            Name of the user
        password:
            Password associated with the user
        database:
            Name of the database you are connecting to

        Returns:
            Object for interacting with the database on the server or none if no connection is established

        Establishes connection to the MySQL database
    """


    try:
        #Establishes a connection to the database on the server and returns an object that allows access to the database
        return mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
    except Error as err:
        #Error handling for a failed connection to the database
        print(f"Error connecting to MySQL database: {err}")
        global error_flag
        error_flag = True
        return None

def check_or_create_user_table(connection, username):
    """
        Args:
            connection:
                Object used for accessing the server

            username:
                String that identifies the user

        
        Makes sure there is a user table and creates one if there isnt
    """


    table_name = f"{username}_notes" #makes a user table using the username
    cursor = connection.cursor()
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'") #Connects to the table
    result = cursor.fetchone() #Checks for first item
    if not result:
        try:
            #If there is no first item it creates a table
            cursor.execute(f"""
                CREATE TABLE {table_name} (
                    note_name VARCHAR(255) NOT NULL,
                    headers TEXT,
                    notes TEXT,
                    bullets TEXT,
                    UNIQUE(note_name)
                )
            """)
            print(f"Table '{table_name}' created successfully.")
        except Error as err:
            #Error handling for failed creation
            print(f"Failed to create table '{table_name}': {err}")
    cursor.close()

def insert_note_data(connection, username, note_name, headers, notes, bullets):
    """
        Args:
            connection:
                Object used for accessing the server

            username:
                String that identifies the user

            note_name:
                String that identifies the note in the database

            headers:
                All of the heading sections of the notes to be stored in the database

            notes:
                All of the notes to be stored in the database

            bullets:
                All of the notes that start with bullet points to be stored in the database
    
        Adds all the note contents to the database in their associated sections.
    """

    table_name = f"{username}_notes"
    cursor = connection.cursor()
    try:
        #Inserts note_name, note headers, notes and bullet points into the database table
        cursor.execute(f"""
            INSERT INTO {table_name} (note_name, headers, notes, bullets)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            headers = VALUES(headers),
            notes = VALUES(notes),
            bullets = VALUES(bullets)
        """, (note_name, str(headers), str(notes), str(bullets)))
        connection.commit()
        print("Note data inserted successfully.")
    except Error as err:
        #If theres an error undoes the changes and prints a message
        connection.rollback()
        print(f"Failed to insert note data: {err}")
    cursor.close()

def main(port, user, password, database, ara_username):
    """
        Args: 
            port: 
                The port number to connect to the MySQL server
            user:
                String that identifies the user
            password: 
                Password associated with the user
            database: 
                Name of the database being used.
            ara_username:
                The username for the created user.

        First ensures connection to the database then stores users note data into the database
    """


    host = 'ix.cs.uoregon.edu'

    # Connect to MySQL Server (without specific database)
    connection = connect_to_mysql(host, port, user, password)
    if connection:
        # Create the database if it does not exist
        create_database_if_not_exists(connection, database)
        connection.close()

    # Connect to the specific database
    db_connection = connect_to_database(host, port, user, password, database)
    if db_connection:
        # Check if user table exists or create new one
        check_or_create_user_table(db_connection, ara_username)
        if ara_username == "Admin":
            # Load in the sample chapter notes
            insert_note_data(db_connection, ara_username, sample_note.note_name, sample_note.headers, sample_note.notes, sample_note.bullets.replace("\n","\\n"))

        # Close the database connection
        db_connection.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
