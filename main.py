from dotenv import load_dotenv
from pymongo import MongoClient
import os
from datetime import date
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv('./config.env')
DB_STRING = os.getenv("DB_CONNECTION_STRING")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
sg = SendGridAPIClient(SENDGRID_API_KEY)

try:
    client = MongoClient(DB_STRING)
    db = client['solershub']
    print("DB CONNECTION SUCCESSFUl")
except Exception as e:
    print("DB CONNECTION ERROR", e)

def birthday_mailer():
    users = list(db['users'].find())
    for user in users:
        if user['birthday'].date() == date.today():
            print("This user's birthday is today", user['email'])
            message = Mail(from_email="0x7lol@gmail.com", to_emails=user['email'], subject="Happy Birthday!!", plain_text_content=f"Dear {user['name']}, we at Solershub wish you a Happy birthday.")
            try:
                sg.send(message)
                print("EMAIL SUCCESSFULY SENT TO ", user["name"], "HERE ", user["email"])
            except Exception as e:
                print("AN ERROR OCCURED WHILE SENDING MAIL", e)

birthday_mailer()