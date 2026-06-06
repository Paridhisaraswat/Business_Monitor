import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv

load_dotenv()

def get_sheet():
    scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
    creds = Credentials.from_service_account_file(
        os.getenv("CREDS_FILE"), scopes=scopes
    )
    client = gspread.authorize(creds)
    return client.open(os.getenv("SHEET_NAME"))

def update_sheets(business):
    sheet = get_sheet()
    all_ws = sheet.worksheet("All Businesses")
    new_ws = sheet.worksheet("New Businesses")

    row = [
        business["place_id"],
        business["name"],
        business["address"],
        business["phone"],
        business["website"],
        business["category"],
        business["postcode"],
        str(business["first_seen"])
    ]

    all_ws.append_row(row)
    new_ws.append_row(row)