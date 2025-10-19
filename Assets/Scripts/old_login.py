import sqlite3
import sys
import random
from cryptography.fernet import Fernet

# --- CONFIG ---
# In a real app, generate and store this securely (not hardcoded)
ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)

# --- INPUT HANDLING ---
try:
    target_email = sys.argv[1]
except IndexError:
    print("Error: No email argument provided.")
    sys.exit(1)


# --- DATABASE SETUP & FUNCTIONS ---
def get_db_connection():
    """Opens a plain SQLite database connection."""
    try:
        connection = sqlite3.connect('game.db')
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        print(f"Database connection error: {e}")
        sys.exit(1)


def setup_table(cursor):
    """Ensures the users table exists."""
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        email BLOB PRIMARY KEY,
        username BLOB NOT NULL
    )
    ''')


def insert_email(connection, cursor, email):
    """Encrypts and inserts user data."""
    try:
        username = f"u{random.randint(100000000, 999999999)}"

        encrypted_email = cipher.encrypt(email.encode())
        encrypted_username = cipher.encrypt(username.encode())

        cursor.execute(
            'INSERT INTO users (email, username) VALUES (?, ?)',
            (encrypted_email, encrypted_username)
        )
        connection.commit()
        print(f"SUCCESS: User {username} inserted for email {email}")
        return True

    except sqlite3.IntegrityError as e:
        print(f"FAIL: Email already exists or integrity error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def show_users(cursor):
    """Helper for debugging: prints decrypted users."""
    cursor.execute('SELECT email, username FROM users')
    for enc_email, enc_username in cursor.fetchall():
        email = cipher.decrypt(enc_email).decode()
        username = cipher.decrypt(enc_username).decode()
        print(f"{email} -> {username}")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    conn, curr = get_db_connection()
    setup_table(curr)
    insert_email(conn, curr, target_email)
    show_users(curr)  # Optional, for checking output
    curr.close()
    conn.close()
    sys.exit(0)
