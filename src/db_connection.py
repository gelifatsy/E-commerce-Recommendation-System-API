# utils/db_connection.py
import os
import psycopg2

def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.
    
    Returns:
        A database connection object.
    """
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "your_database")
    user = os.getenv("POSTGRES_USER", "your_username")
    password = os.getenv("POSTGRES_PASSWORD", "your_password")

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error connecting to the PostgreSQL database:", error)
        raise