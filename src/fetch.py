import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_businesses(postcode, category):
    query = f"{category} in {postcode} India"
    params = {
        "engine": "google_maps",
        "q": query,
        "type": "search",
        "api_key": os.getenv("SERPAPI_KEY")
    }
    response = requests.get("https://serpapi.com/search.json", params=params)
    data = response.json()

    businesses = []
    for r in data.get("local_results", []):
        businesses.append({
            "place_id": r.get("place_id", ""),
            "name": r.get("title", ""),
            "address": r.get("address", ""),
            "phone": r.get("phone", ""),
            "website": r.get("website", ""),
            "category": category,
            "postcode": postcode,
            "first_seen": None
        })
    return businesses