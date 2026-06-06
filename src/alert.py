import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(new_businesses):
    body = "New businesses found:\n\n"
    for b in new_businesses:
        body += f"Name: {b['name']}\n"
        body += f"Address: {b['address']}\n"
        body += f"Phone: {b['phone']}\n"
        body += f"Website: {b['website']}\n"
        body += f"Category: {b['category']}\n"
        body += f"Postcode: {b['postcode']}\n"
        body += "-" * 40 + "\n"

    msg = MIMEText(body)
    msg["Subject"] = f"🆕 {len(new_businesses)} New Business(es) Found"
    msg["From"] = os.getenv("EMAIL_SENDER")
    msg["To"] = os.getenv("EMAIL_RECEIVER")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)
    
    print(f"Email alert sent for {len(new_businesses)} new businesses!")