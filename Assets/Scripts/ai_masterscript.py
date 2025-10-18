import sqlcipher3.dbapi2 as sqlcipher
import sys
import random
import smtplib
import ssl
from email.message import EmailMessage
from email.mime.text import MIMEText # Included for completeness, though EmailMessage is used below

# --- CONFIGURATION ---
# Database Setup
ENCRYPTION_KEY = 'TEMP_HACKATHON_KEY'
DATABASE_FILE = 'game.db'

# Email Setup
EMAIL_SENDER = 'smtp41290@gmail.com' # Replace with your sender email
# NOTE: This 'App Password' is highly sensitive. For real-world use,
# store it securely (e.g., environment variables) and NEVER in source code.
EMAIL_APP_PASSWORD = 'tmtq ukqn dsdr ozro' # Replace with your generated App Password

# --- INPUT HANDLING ---
# The email is expected as the first command-line argument (sys.argv[1])
try:
    target_email = sys.argv[1]
except IndexError:
    # If no email is provided, exit with an error code
    print("Error: No email argument provided.")
    print("Usage: python script_name.py <recipient_email>")
    sys.exit(1)

# --- DATABASE SETUP & FUNCTIONS ---

def get_db_connection():
    """Establishes connection to the encrypted database and executes PRAGMA key."""
    try:
        connection = sqlcipher.connect(DATABASE_FILE)
        cursor = connection.cursor()
        # The key is passed directly in the string
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
        print(f"DATABASE: SUCCESS: User {username} inserted for email {email}")
        return True
    except sqlcipher.IntegrityError:
        # This catches duplicate emails or usernames. We assume existing is fine for login.
        print(f"DATABASE: User for email {email} already exists. Proceeding.")
        return True # Return True to proceed with the OTP email
    except Exception as e:
        print(f"DATABASE: An unexpected error occurred during insertion: {e}")
        return False

# --- EMAIL FUNCTION ---

def send_password(recipient_email, sender, password):
    """Generates an OTP and sends it via email."""
    otp = random.randint(100000, 999999)

    # 1. Create the HTML content
    html_content = f"""
    <html>
        <body>
            <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                <h2 style="color: #1a73e8;">Your One-Time Password (OTP)</h2>
                <p>Hello,</p>
                <p>Use the following code to complete your login or transaction:</p>
                <div style="background-color: #f0f0f0; padding: 15px; border-radius: 4px; font-size: 24px; text-align: center; margin: 20px 0;">
                    <strong>{otp}</strong>
                </div>
                <p style="color: #888;">This code is valid for a short time only. Please do not share this code with anyone.</p>
                <p>Thank you.</p>
            </div>
        </body>
    </html>
    """

    # 2. Create the email message
    email_msg = EmailMessage()
    email_msg['From'] = sender
    email_msg['To'] = recipient_email
    email_msg['Subject'] = "🔒 Your One-Time Password (OTP)"

    # Attach both plain text and HTML (best practice)
    email_msg.set_content(f"Your OTP is: {otp}. Please do not share this code.")
    email_msg.add_alternative(html_content, subtype='html')

    # 3. Send the email
    try:
        context = ssl.create_default_context()
        # Connect to the Google SMTP server over SSL (port 465)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipient_email, email_msg.as_string())
        print(f"EMAIL: SUCCESS: OTP sent to {recipient_email}. OTP: {otp}")
        return otp
    except smtplib.SMTPAuthenticationError:
        print("EMAIL: FAIL: Authentication failed. Check sender email or app password.")
        print("NOTE: You must use a Google App Password, not your regular password.")
    except Exception as e:
        print(f"EMAIL: FAIL: An unexpected error occurred while sending email: {e}")
    
    return None


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    
    # 1. Database connection and setup
    conn, curr = get_db_connection()
    setup_table(curr)

    # 2. Attempt to insert/register the user
    # The function returns True if the user is registered OR already exists.
    registration_successful = insert_email(conn, curr, target_email)

    # 3. Close database connection
    curr.close()
    conn.close()

    # 4. Send the OTP email if registration/check was successful
    if registration_successful:
        print("\nAttempting to send OTP email...")
        otp = send_password(target_email, EMAIL_SENDER, EMAIL_APP_PASSWORD)
        
        if otp is not None:
            sys.exit(0) # Exit successfully
        else:
            sys.exit(2) # Exit with an error code for email failure

    # If registration failed for another reason (e.g., unexpected database error)
    sys.exit(1)
