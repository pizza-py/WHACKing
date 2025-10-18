import sqlcipher3.dbapi2 as sqlcipher
import sys
import random

# --- CONFIG ---
ENCRYPTION_KEY = 'TEMP_HACKATHON_KEY'

# The email is expected as the first command-line argument (sys.argv[1])
# We will get an IndexError if no argument is provided, so we wrap it.
try:
    target_email = sys.argv[1]
except IndexError:
    # If no email is provided, exit with an error code
    print("Error: No email argument provided.")
    sys.exit(1)


# --- DATABASE SETUP & FUNCTIONS ---
def get_db_connection():
    """Establishes connection and executes PRAGMA key."""
    try:
        connection = sqlcipher.connect('game.db')
        cursor = connection.cursor()
        cursor.execute(f"PRAGMA key = '{ENCRYPTION_KEY}';")
        return connection, cursor
    except Exception as e:
        print(f"Database connection error: {e}")
        sys.exit(1)


def setup_table(cursor):
    """Ensures the users table exists."""
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL
    )
    ''')


def insert_email(connection, cursor, email):
    """Inserts a new user with a random username."""
    try:
        username = f"u{random.randint(100000000, 999999999)}"
        cursor.execute(
            'INSERT INTO users (email, username) VALUES (?, ?)',
            (email, username)
        )
        connection.commit()
        print(f"SUCCESS: User {username} inserted for email {email}")
        return True
    except sqlcipher.IntegrityError as e:
        # This will catch duplicate emails or usernames.
        # For simplicity, we assume an existing email is fine and skip insertion.
        print(f"FAIL: Email {email} already exists or integrity error: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during insertion: {e}")
        return False


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    conn, curr = get_db_connection()
    setup_table(curr)

    # Note: We are assuming a successful 'login' attempt means
    # the user is logging in for the *first time* and should be created.
    # The original C# script implies 'login' is also 'registration' for the demo.

    insert_email(conn, curr, target_email)

    curr.close()
    conn.close()
    sys.exit(0) # Exit successfully'''
