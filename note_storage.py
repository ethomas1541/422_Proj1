import mysql.connector
from mysql.connector import Error
import samplepdf


error_flag = False

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
        global error_flag
        error_flag = True
        return None

def connect_to_database(host, port, user, password, database):
    try:
        return mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
    except Error as err:
        print(f"Error connecting to MySQL database: {err}")
        global error_flag
        error_flag = True
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
                    note_name VARCHAR(255) NOT NULL,
                    headers TEXT,
                    notes TEXT,
                    bullets TEXT,
                    UNIQUE(note_name)
                )
            """)
            print(f"Table '{table_name}' created successfully.")
        except Error as err:
            print(f"Failed to create table '{table_name}': {err}")
    cursor.close()

def insert_note_data(connection, username, note_name, headers, notes, bullets):
    table_name = f"{username}_notes"
    cursor = connection.cursor()
    try:
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
        connection.rollback()
        print(f"Failed to insert note data: {err}")
    cursor.close()

def main(port, user, password, database, ara_username):
    host = 'ix.cs.uoregon.edu'
    """
    port = 3854
    user = 'dtweedale'
    password = 'password'
    database = input("Enter a name for the database:")
    """

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
            insert_note_data(db_connection, ara_username, samplepdf.note_name, samplepdf.headers, samplepdf.notes, samplepdf.bullets.replace("\n","\\n"))

        # Close the database connection
        db_connection.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()