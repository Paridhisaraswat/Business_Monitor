import time
from datetime import datetime
from src.fetch import fetch_businesses
from src.database import setup_database, is_new_business, save_business
from src.sheets import get_sheet, update_sheets
from src.alert import send_email

# Postcode and category combinations to scan
SEARCHES = [
    {"postcode": "302001", "category": "restaurant"},
    {"postcode": "302001", "category": "cafe"},
]

def run():
    print("Setting up database...")
    setup_database()

    print("Connecting to Google Sheets...")
    sheet = get_sheet()
    all_ws = sheet.worksheet("All Businesses")
    new_ws = sheet.worksheet("New Businesses")
    log_ws = sheet.worksheet("Alert Log")
    config_ws = sheet.worksheet("Config")

    # Clear new businesses tab for today
    new_ws.clear()
    time.sleep(1)
    new_ws.append_row(["Place ID", "Name", "Address", "Phone", "Website", "Category", "Postcode", "First Seen"])
    time.sleep(1)

    new_businesses = []

    for search in SEARCHES:
        postcode = search["postcode"]
        category = search["category"]
        print(f"Scanning {category} in {postcode}...")

        businesses = fetch_businesses(postcode, category)
        print(f"Found {len(businesses)} businesses from API")

        for b in businesses:
            if not b["place_id"]:
                continue

            if is_new_business(b["place_id"]):
                b["first_seen"] = datetime.now()
                save_business(b)

                row = [
                    b["place_id"],
                    b["name"],
                    b["address"],
                    b["phone"],
                    b["website"],
                    b["category"],
                    b["postcode"],
                    str(b["first_seen"])
                ]
                all_ws.append_row(row)
                time.sleep(1)
                new_ws.append_row(row)
                time.sleep(1)
                new_businesses.append(b)
                print(f"New business found: {b['name']}")
            else:
                print(f"Already known: {b['name']}")

        # Update last scanned in Config sheet
        for i, row in enumerate(config_ws.get_all_values()):
            if row[0].strip() == postcode.strip() and row[1].strip().lower() == category.strip().lower():
                config_ws.update_cell(i + 1, 3, str(datetime.now()))
                time.sleep(1)
                break

    # Update Alert Log
    log_ws.append_row([
        str(datetime.now()),
        len(new_businesses),
        "Alert Sent" if new_businesses else "No Alert"
    ])
    time.sleep(1)

    # Send email if new businesses found
    if new_businesses:
        send_email(new_businesses)
    else:
        print("No new businesses found today.")

    print(f"Done! {len(new_businesses)} new businesses found.")

if __name__ == "__main__":
    run()