from sqlcipher3 import dbapi2 as sqlcipher
import os  # Needed to access environment variables
import random

# --- CONFIG ---
# WARNING: For the hackathon, we are hardcoding a consistent key for stability.
# For production, this MUST be loaded securely via os.environ.get()
ENCRYPTION_KEY = 'TEMP_HACKATHON_KEY'  # Using a single, stable key for consistency

connection = sqlcipher.connect('game.db')
cursor = connection.cursor()

# 1. ENCRYPTION KEY EXECUTION
# This line is essential for SQLCipher: it uses the key to decrypt or create the database.
cursor.execute(f"PRAGMA key = '{ENCRYPTION_KEY}';")

##just run this at the start to make sure that the table has been executed
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL
    -- Removed is_active and CHECK constraint to meet minimal schema requirement.
)
''')


# function which checks to see if there is already an associated account
# returns TRUE if there is already an email in the system, FALSE if there isn't
def check_email(email):
    # This selects the email if it exists
    cursor.execute('''SELECT email FROM users WHERE email = ?''', (email,))

    result = cursor.fetchone()

    if result is None:
        return False
    else:
        return True


# function which adds new
def insert_email(email):
    try:
        username = f"u{random.randint(100000000,999999999)}"
        # FIX: Ensure we insert ONLY the two columns: email and username
        cursor.execute(
            'INSERT INTO users (email, username) VALUES (?, ?)',
            (email, username)
        )
        print(f"Successfully inserted user: {username}")
        connection.commit()  # FIX: Ensure commit happens inside the successful block

    except sqlcipher.IntegrityError as e:
        # This will catch duplicate emails (PRIMARY KEY) or usernames (UNIQUE)
        print(f"Insertion Failed (Integrity Error): {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")





# Note: The commit is now inside the insert_email function to ensure changes are saved only upon success.
connection.commit()
cursor.close()
connection.close()

#after executing this script the users details should be in the system
