def map_event(event):
    try:
        return {
            "id": event.get("id"),
            "name": event.get("name"),
            "date": event.get("dates", {}).get("start", {}).get("localDate"),
            "time": event.get("dates", {}).get("start", {}).get("localTime"),
            "venue": event.get("_embedded", {}).get("venues", [{}])[0].get("name"),
            "city": event.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name"),
            "image": event.get("images", [{}])[0].get("url"),
            "url": event.get("url"),
            "source": "Ticketmaster"
        }
    except Exception:
        return None


def map_bookmyshow_event(event):
    """Map BookMyShow event to standard format"""
    try:
        return {
            "id": event.get("eventId") or event.get("id"),
            "name": event.get("eventTitle") or event.get("name"),
            "date": event.get("eventDate") or event.get("date"),
            "time": event.get("eventTime") or event.get("time", "N/A"),
            "venue": event.get("venueName") or event.get("venue", "N/A"),
            "city": event.get("city") or "N/A",
            "image": event.get("imageUrl") or event.get("image"),
            "url": event.get("eventUrl") or event.get("url"),
            "source": "BookMyShow"
        }
    except Exception:
        return None
