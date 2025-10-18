import smtplib
import ssl
from email.message import EmailMessage
from email.mime.text import MIMEText  # You'll need this for HTML
import random

def send_password( recipient_email):
    otp = random.randint(100000,999999)
    # Your credentials
    email_sender = 'smtp41290@gmail.com'
    email_app_password = 'tmtq ukqn dsdr ozro'

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
    email = EmailMessage()
    email['From'] = email_sender
    email['To'] = recipient_email
    email['Subject'] = "🔒 Your One-Time Password (OTP)"

    # 3. Attach both plain text and HTML (best practice)
    # Plain text version (for clients that don't support HTML)
    email.set_content(f"Your OTP is: {otp}. Please do not share this code.")

    # HTML version (the one that will display nicely)
    email.add_alternative(html_content, subtype='html')

    # Setting up the email server connection
    context = ssl.create_default_context()
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)

    smtp_server.login(email_sender, email_app_password)

    # Send the email and close the connection
    smtp_server.sendmail(email_sender, recipient_email, email.as_string())
    smtp_server.quit()
    return otp #this returns the otp to the c# program


# Example usage (if you want to test it):
send_password( 'your_email')



