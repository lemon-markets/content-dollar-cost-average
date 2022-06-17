import os
import smtplib
from email.message import EmailMessage
import ssl
from dotenv import load_dotenv

load_dotenv()
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

class Email():

    def send_email(avg_price):
        body = """
        Your current average price is 
        """ + str(avg_price)

        smtp_server = "smtp.gmail.com"
        message = EmailMessage()
        message['Subject'] = 'Your Dollar Cost Averaging Bot Report'
        message['From'] = EMAIL_ADDRESS
        message['To'] = ["eric.tang@lemon.markets"]
        message.set_content(body, 'plain')
        default_context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port=465, context=default_context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)
