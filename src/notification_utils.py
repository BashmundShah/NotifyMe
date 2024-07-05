from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
from_email = os.getenv("FROM_EMAIL")

default_to_emails = ["bashmundkhan@yahoo.com", "mariyahassan.akhter@gmail.com"]
default_subject = "Appointment is available! - NotifyMe"
default_content = "An appointment is available at the Ausländeramt Aachen Team-1. Book now! https://termine.staedteregion-aachen.de/auslaenderamt/"


def send_email_via_sendgrid(
    to_emails=default_to_emails,
    subject=default_subject,
    content=default_content,
):
    """
    Sends an email using SendGrid.

    Parameters:
    - to_emails (str or list): Recipient email address(es).
    - subject (str): Email subject.
    - content (str): Email content.
    - from_email (str): Sender's email address.
    - sendgrid_api_key (str): Your SendGrid API key.
    """
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=content,
    )
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(f"Email sent. Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email: {e}")
