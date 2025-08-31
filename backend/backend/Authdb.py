import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'recruitmetrics.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create scores table to save user results
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        score REAL NOT NULL,
        gpa REAL NOT NULL,
        height TEXT NOT NULL,
        position TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()

class User:
    @staticmethod
    def create(username, email, password):
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Username or email already exists
            return False
        finally:
            conn.close()

    @staticmethod
    def authenticate(email, password):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password_hash FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            return {"id": user[0], "username": user[1]}
        return None
    
    @staticmethod
    def save_score(user_id, score_data):
        conn = None
        try:
            required_fields = ['score', 'gpa', 'height', 'position']
            for field in required_fields:
                if field not in score_data:
                    return False
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO scores (user_id, score, gpa, height, position) VALUES (?, ?, ?, ?, ?)",
                (user_id, score_data['score'], score_data['gpa'], score_data['height'], score_data['position'])
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            # Log the error
            print(f"Database error: {e}")
            return False
        finally:
            if conn:
                conn.close()