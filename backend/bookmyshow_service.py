import requests
from datetime import datetime, timedelta
import random

def get_events_by_city_bookmyshow(city):
    """
    Fetch events from BookMyShow
    Since BookMyShow doesn't have a public API, we provide sample data
    In production, you would use web scraping or official API if available
    """
    
    try:
        # Try to fetch from BookMyShow website if possible
        # Otherwise return sample data
        events = fetch_bookmyshow_events(city)
        return events
    except Exception as e:
        print(f"Error fetching from BookMyShow: {e}")
        # Return sample events as fallback
        return get_sample_bookmyshow_events(city)


def fetch_bookmyshow_events(city):
    """
    Attempt to fetch real events from BookMyShow
    """
    try:
        # BookMyShow search URL structure
        city_slug = city.lower().replace(" ", "-")
        url = f"https://in.bookmyshow.com/{city_slug}/events"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            # If we can parse the page, extract events
            # This is a simplified version - real implementation would parse HTML
            return get_sample_bookmyshow_events(city)
        else:
            return []
    except Exception as e:
        print(f"Error in fetch_bookmyshow_events: {e}")
        return []


def get_sample_bookmyshow_events(city):
    """
    Return sample BookMyShow events for demonstration
    In production, replace with actual API call or web scraping
    """
    
    sample_events = {
        "london": [
            {
                "id": "bms_001_london",
                "name": "The Lion King - Musical Show",
                "date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                "time": "19:30",
                "venue": "West End Theatre, London",
                "city": "London",
                "image": "https://images.bookmyshow.com/poster/320x480/london_lion_king.jpg",
                "url": "https://in.bookmyshow.com/london/events",
                "source": "BookMyShow"
            },
            {
                "id": "bms_002_london",
                "name": "Comedy Night Stand-Up",
                "date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                "time": "20:00",
                "venue": "Comedy Club London",
                "city": "London",
                "image": "https://images.bookmyshow.com/poster/320x480/comedy_night.jpg",
                "url": "https://in.bookmyshow.com/london/events",
                "source": "BookMyShow"
            },
            {
                "id": "bms_003_london",
                "name": "Jazz Festival Live",
                "date": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
                "time": "18:00",
                "venue": "Royal Albert Hall",
                "city": "London",
                "image": "https://images.bookmyshow.com/poster/320x480/jazz_festival.jpg",
                "url": "https://in.bookmyshow.com/london/events",
                "source": "BookMyShow"
            }
        ],
        "paris": [
            {
                "id": "bms_004_paris",
                "name": "Moulin Rouge Cabaret",
                "date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                "time": "21:00",
                "venue": "Moulin Rouge",
                "city": "Paris",
                "image": "https://images.bookmyshow.com/poster/320x480/moulin_rouge.jpg",
                "url": "https://in.bookmyshow.com/paris/events",
                "source": "BookMyShow"
            },
            {
                "id": "bms_005_paris",
                "name": "French Cinema Festival",
                "date": (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d"),
                "time": "19:00",
                "venue": "Cinema Paradiso",
                "city": "Paris",
                "image": "https://images.bookmyshow.com/poster/320x480/cinema_festival.jpg",
                "url": "https://in.bookmyshow.com/paris/events",
                "source": "BookMyShow"
            }
        ],
        "new york": [
            {
                "id": "bms_006_ny",
                "name": "Broadway Musical Night",
                "date": (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d"),
                "time": "20:00",
                "venue": "Broadway Theatre",
                "city": "New York",
                "image": "https://images.bookmyshow.com/poster/320x480/broadway.jpg",
                "url": "https://in.bookmyshow.com/newyork/events",
                "source": "BookMyShow"
            },
            {
                "id": "bms_007_ny",
                "name": "NY Comedy Club Tour",
                "date": (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d"),
                "time": "21:00",
                "venue": "Comedy Cellar NYC",
                "city": "New York",
                "image": "https://images.bookmyshow.com/poster/320x480/comedy_club.jpg",
                "url": "https://in.bookmyshow.com/newyork/events",
                "source": "BookMyShow"
            }
        ],
        "tokyo": [
            {
                "id": "bms_008_tokyo",
                "name": "Tokyo Gaming Expo",
                "date": (datetime.now() + timedelta(days=9)).strftime("%Y-%m-%d"),
                "time": "10:00",
                "venue": "Tokyo Convention Center",
                "city": "Tokyo",
                "image": "https://images.bookmyshow.com/poster/320x480/gaming_expo.jpg",
                "url": "https://in.bookmyshow.com/tokyo/events",
                "source": "BookMyShow"
            }
        ],
        "sydney": [
            {
                "id": "bms_009_sydney",
                "name": "Sydney Opera House Concert",
                "date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                "time": "19:30",
                "venue": "Sydney Opera House",
                "city": "Sydney",
                "image": "https://images.bookmyshow.com/poster/320x480/opera_concert.jpg",
                "url": "https://in.bookmyshow.com/sydney/events",
                "source": "BookMyShow"
            }
        ],
        "default": [
            {
                "id": "bms_default_1",
                "name": "Concert Event",
                "date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                "time": "19:00",
                "venue": "Local Concert Hall",
                "city": city,
                "image": "https://images.bookmyshow.com/poster/320x480/concert.jpg",
                "url": "https://in.bookmyshow.com/events",
                "source": "BookMyShow"
            },
            {
                "id": "bms_default_2",
                "name": "Cultural Show",
                "date": (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d"),
                "time": "18:30",
                "venue": "Cultural Center",
                "city": city,
                "image": "https://images.bookmyshow.com/poster/320x480/cultural.jpg",
                "url": "https://in.bookmyshow.com/events",
                "source": "BookMyShow"
            }
        ]
    }
    
    city_lower = city.lower()
    
    # Return events for the city if available, otherwise return default events
    if city_lower in sample_events:
        return sample_events[city_lower]
    else:
        # Return default events for any city
        default = sample_events["default"]
        # Add more variety with random generation
        return default[:2]  # Return at least the default events

