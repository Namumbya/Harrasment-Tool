import sqlite3
import jwt
import datetime

def init_auth_db():
    conn = sqlite3.connect('harassment_reports.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

def verify_jwt_token(token):
    try:
        # Replace with your actual secret key
        secret_key = "your-secret-key"
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except:
        return None 