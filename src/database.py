import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def setup_database():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}")
    cursor.execute(f"USE {os.getenv('DB_NAME')}")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS businesses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            place_id VARCHAR(255) UNIQUE,
            name VARCHAR(255),
            address TEXT,
            phone VARCHAR(50),
            website VARCHAR(255),
            category VARCHAR(100),
            postcode VARCHAR(20),
            first_seen DATETIME
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def is_new_business(place_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM businesses WHERE place_id = %s", (place_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is None

def save_business(business):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT IGNORE INTO businesses 
        (place_id, name, address, phone, website, category, postcode, first_seen)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        business["place_id"],
        business["name"],
        business["address"],
        business["phone"],
        business["website"],
        business["category"],
        business["postcode"],
        business["first_seen"]
    ))
    conn.commit()
    cursor.close()
    conn.close()