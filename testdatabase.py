import mysql.connector
from mysql.connector import Error

def create_database_if_not_exists(connection, database_name):
    cursor = connection.cursor()
    cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")
    result = cursor.fetchone()
    if not result:
        try:
            cursor.execute(f"CREATE DATABASE {database_name}")
            print(f"Database '{database_name}' created successfully.")
        except Error as err:
            print(f"Failed to create database '{database_name}': {err}")
    cursor.close()

def connect_to_mysql(host, port, user, password):
    try:
        return mysql.connector.connect(host=host, port=port, user=user, password=password)
    except Error as err:
        print(f"Error connecting to MySQL Server: {err}")
        return None

def connect_to_database(host, port, user, password, database):
    try:
        return mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
    except Error as err:
        print(f"Error connecting to MySQL database: {err}")
        return None

def check_or_create_user_table(connection, username):
    table_name = f"{username}_notes"
    cursor = connection.cursor()
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchone()
    if not result:
        try:
            cursor.execute(f"""
                CREATE TABLE {table_name} (
                    note_id INT AUTO_INCREMENT PRIMARY KEY,
                    note_name VARCHAR(255) NOT NULL,
                    subject VARCHAR(255) NOT NULL,
                    note TEXT NOT NULL
                )
            """)
            print(f"Table '{table_name}' created successfully.")
        except Error as err:
            print(f"Failed to create table '{table_name}': {err}")
    cursor.close()

def main():
    host = 'ix.cs.uoregon.edu'
    port = 3854
    user = 'dtweedale'
    password = 'password'
    database = input("Enter a name for the database:")

    # Connect to MySQL Server (without specific database)
    connection = connect_to_mysql(host, port, user, password)
    if connection:
        # Create the database if it does not exist
        create_database_if_not_exists(connection, database)
        connection.close()

    # Connect to the specific database
    db_connection = connect_to_database(host, port, user, password, database)
    if db_connection:
        # Ask user for their username
        username = input("Enter your username: ")
        # Check if user table exists or create new one
        check_or_create_user_table(db_connection, username)

        # Close the database connection
        db_connection.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()