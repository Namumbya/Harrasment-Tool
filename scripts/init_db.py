import sqlite3
from sqlite3 import Error

def create_tables():
    try:
        # Connect to SQLite (this will create the database if it doesn't exist)
        connection = sqlite3.connect('harassment_tool.db')
        cursor = connection.cursor()
        
        # Create resources table
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            contact TEXT,
            address TEXT,
            latitude REAL,
            longitude REAL,
            description TEXT
        );
        '''
        
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully!")
        
    except Error as error:
        print("Error while creating the database:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("SQLite connection closed")

if __name__ == "__main__":
    create_tables() 