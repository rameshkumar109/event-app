import requests
from config import API_KEY, BASE_URL
from models import map_event

def get_events_by_city(city):

    params = {
        "apikey": API_KEY,
        "city": city,
        "size": 10
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)

        if response.status_code != 200:
            return []

        data = response.json()

        events = data.get("_embedded", {}).get("events", [])

        cleaned_events = []
        for event in events:
            mapped = map_event(event)
            if mapped:
                cleaned_events.append(mapped)

        return cleaned_events

    except requests.exceptions.RequestException:
        return []
