import requests
from datetime import datetime, timedelta
from config import PREDICTHQ_API_KEY

BASE_URL = "https://api.predicthq.com/v1/events"

def get_events_by_city_predicthq(city):
    """
    Fetch events from PredictHQ API
    PredictHQ is a global events data provider with a comprehensive API
    """
    
    if not PREDICTHQ_API_KEY:
        print("PredictHQ API key not configured")
        return []
    
    try:
        # Set date range (next 30 days)
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        params = {
            "q": city,
            "active.gte": start_date,
            "active.lte": end_date,
            "limit": 20,
            "sort": ["-rank"],
            "category": ["concerts", "expos", "performing-arts", "sports"]
        }
        
        headers = {
            "Authorization": f"Bearer {PREDICTHQ_API_KEY}",
            "Accept": "application/json"
        }
        
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"PredictHQ API error: {response.status_code}")
            return []
        
        data = response.json()
        events = []
        
        for event in data.get("results", []):
            mapped = map_predicthq_event(event)
            if mapped:
                events.append(mapped)
        
        return events
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from PredictHQ: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error in PredictHQ service: {e}")
        return []


def map_predicthq_event(event):
    """
    Map PredictHQ event data to our standard format
    """
    try:
        # Extract location information
        location = event.get("location", {})
        city = None
        
        if location:
            if isinstance(location, dict):
                city = location.get("city")
            elif isinstance(location, list) and len(location) > 0:
                city = location[0].get("city") if isinstance(location[0], dict) else None
        
        # Extract date and time
        start_date = event.get("start", "")
        if start_date:
            start_date = start_date.split("T")[0]  # Get only the date part
        
        start_time = ""
        if "T" in event.get("start", ""):
            start_time = event.get("start", "").split("T")[1].split("+")[0]  # Get time part
        
        # Extract image with multiple fallback options
        image = None
        
        # Try to get image from entities first
        if "entities" in event and event["entities"]:
            for entity in event["entities"]:
                if entity.get("image"):
                    image = entity.get("image")
                    break
        
        # If no image from entities, try other sources
        if not image:
            # Try direct image field
            image = event.get("image")
        
        # If still no image, generate based on category
        if not image:
            category = event.get("category", "general")
            image = get_category_image(category)
        
        # Final fallback - use placeholder with category
        if not image:
            category = event.get("category", "general")
            image = f"https://via.placeholder.com/320x480?text={category.replace('-', '%20').title()}"
        
        return {
            "id": event.get("id", ""),
            "name": event.get("title", "Event"),
            "date": start_date,
            "time": start_time or "TBD",
            "venue": event.get("venue", {}).get("name") if isinstance(event.get("venue"), dict) else "TBD",
            "city": city or "Unknown",
            "image": image,
            "url": event.get("url") or f"https://www.predicthq.com/events/{event.get('id')}",
            "source": "PredictHQ",
            "category": event.get("category", "general"),
            "rank": event.get("rank", 0)
        }
    except Exception as e:
        print(f"Error mapping PredictHQ event: {e}")
        return None


def get_category_image(category):
    """
    Get a representative image URL based on event category
    """
    category_images = {
        "concerts": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=500&h=700&fit=crop",
        "expos": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=500&h=700&fit=crop",
        "performing-arts": "https://images.unsplash.com/photo-1501612780212-51817c2750b9?w=500&h=700&fit=crop",
        "sports": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=500&h=700&fit=crop",
        "festivals": "https://images.unsplash.com/photo-1533900298318-6b8da08a523e?w=500&h=700&fit=crop",
        "conferences": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=500&h=700&fit=crop",
        "comedy": "https://images.unsplash.com/photo-1514306688772-e0cb64a2c082?w=500&h=700&fit=crop",
        "theater": "https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=500&h=700&fit=crop",
        "movies": "https://images.unsplash.com/photo-1489599849228-ed56787a2b78?w=500&h=700&fit=crop",
        "general": "https://images.unsplash.com/photo-1456735190898-61de99a46e00?w=500&h=700&fit=crop"
    }
    
    # Try to find a matching category
    for key, url in category_images.items():
        if key.lower() in category.lower() or category.lower() in key.lower():
            return url
    
    # Return default if no match
    return category_images.get("general")

