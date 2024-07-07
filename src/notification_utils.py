from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
import telegram

# Load environment variables from .env file
load_dotenv()

# Access the API key
sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
from_email = os.getenv("FROM_EMAIL")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

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


async def send_telegram_message():
    """
    Sends a message to a Telegram chat using a bot.

    Parameters:
    - chat_id (str): The chat ID where the message will be sent.
    - message (str): The message to send.
    - bot_token (str, optional): The Telegram bot token. If not provided, it will be read from the TELEGRAM_BOT_TOKEN environment variable.
    """

    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=default_content)
