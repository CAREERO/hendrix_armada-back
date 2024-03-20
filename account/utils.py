# accounts/utils.py
from django.core.mail import EmailMessage

def send_welcome_email(email):
    subject = 'Welcome to Your Website'
    message = 'Thank you for registering on our website!'
    from_email = 'your@email.com'  # Replace with your email
    to_email = [email]

    email = EmailMessage(subject, message, from_email, to_email)
    email.send()
