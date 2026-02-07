import os
import secrets
from urllib.parse import urlencode
import requests
from flask import Flask, request, jsonify, redirect, make_response
from dotenv import load_dotenv

# Load environment variables from backend/.env for local development
load_dotenv()
from flask_cors import CORS
from ticketmaster_service import get_events_by_city
from bookmyshow_service import get_events_by_city_bookmyshow
from predicthq_service import get_events_by_city_predicthq
from countries_service import get_country_suggestions, get_all_countries, get_countries_by_region
from cities_service import (
    get_city_suggestions, get_all_cities, get_cities_by_region, 
    get_cities_by_country, get_available_regions, get_available_countries
)
from auth_service import create_user, get_user_by_email, verify_password, create_token_for_user, decode_token

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-flask-secret")
CORS(app)  # allow frontend later

# Google OAuth config
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv(
    "GOOGLE_REDIRECT_URI",
    "http://127.0.0.1:5000/auth/google/callback"
)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


@app.route("/")
def home():
    return {
        "message": "event-app Backend Running",
        "available_endpoints": {
            "events": "GET /events?city=<city>&source=all",
            "countries": "GET /countries or /countries?search=<letter>",
            "regions": "GET /countries/regions"
        },
        "sources": ["ticketmaster", "bookmyshow", "predicthq"]
    }


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "event-app Backend"}


@app.route("/events", methods=["GET"])
def events():
    """Get events from specified sources (default: all)"""
    city = request.args.get("city")
    source = request.args.get("source", "all")  # all, ticketmaster, bookmyshow, predicthq

    if not city:
        return jsonify({"error": "City parameter required"}), 400

    all_events = []

    # Fetch from Ticketmaster if requested
    if source in ["all", "ticketmaster"]:
        try:
            ticketmaster_events = get_events_by_city(city)
            all_events.extend(ticketmaster_events)
        except Exception as e:
            print(f"Error fetching Ticketmaster events: {e}")

    # Fetch from BookMyShow if requested
    if source in ["all", "bookmyshow"]:
        try:
            bookmyshow_events = get_events_by_city_bookmyshow(city)
            all_events.extend(bookmyshow_events)
        except Exception as e:
            print(f"Error fetching BookMyShow events: {e}")

    # Fetch from PredictHQ if requested
    if source in ["all", "predicthq"]:
        try:
            predicthq_events = get_events_by_city_predicthq(city)
            all_events.extend(predicthq_events)
        except Exception as e:
            print(f"Error fetching PredictHQ events: {e}")

    return jsonify({
        "city": city,
        "source": source,
        "count": len(all_events),
        "events": all_events
    })


@app.route("/events/ticketmaster", methods=["GET"])
def events_ticketmaster():
    """Get events only from Ticketmaster"""
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City parameter required"}), 400

    try:
        events = get_events_by_city(city)
        return jsonify({
            "city": city,
            "source": "Ticketmaster",
            "count": len(events),
            "events": events
        })
    except Exception as e:
        return jsonify({"error": f"Failed to fetch Ticketmaster events: {str(e)}"}), 500


@app.route("/events/bookmyshow", methods=["GET"])
def events_bookmyshow():
    """Get events only from BookMyShow"""
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City parameter required"}), 400

    try:
        events = get_events_by_city_bookmyshow(city)
        return jsonify({
            "city": city,
            "source": "BookMyShow",
            "count": len(events),
            "events": events
        })
    except Exception as e:
        return jsonify({"error": f"Failed to fetch BookMyShow events: {str(e)}"}), 500


@app.route("/events/predicthq", methods=["GET"])
def events_predicthq():
    """Get events only from PredictHQ"""
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City parameter required"}), 400

    try:
        events = get_events_by_city_predicthq(city)
        return jsonify({
            "city": city,
            "source": "PredictHQ",
            "count": len(events),
            "events": events
        })
    except Exception as e:
        return jsonify({"error": f"Failed to fetch PredictHQ events: {str(e)}"}), 500


@app.route("/sources", methods=["GET"])
def available_sources():
    """Get available event sources"""
    return jsonify({
        "sources": [
            {
                "name": "Ticketmaster",
                "endpoint": "/events/ticketmaster",
                "emoji": "🎭",
                "description": "Live entertainment ticketing platform"
            },
            {
                "name": "BookMyShow",
                "endpoint": "/events/bookmyshow",
                "emoji": "🎬",
                "description": "Entertainment ticketing platform for movies, events, and shows"
            },
            {
                "name": "PredictHQ",
                "endpoint": "/events/predicthq",
                "emoji": "🌍",
                "description": "Global event data and prediction platform"
            }
        ]
    })


@app.route("/countries", methods=["GET"])
def countries():
    """
    Get country suggestions or all countries
    Query parameters:
    - search: Filter countries by name (starting with letter/text)
    - region: Filter by region
    """
    search = request.args.get("search", "").strip()
    region = request.args.get("region", "").strip()
    
    try:
        if search:
            # Get suggestions based on search text
            suggestions = get_country_suggestions(search)
            return jsonify({
                "type": "suggestions",
                "search": search,
                "count": len(suggestions),
                "countries": suggestions
            })
        elif region:
            # Get countries by region
            countries_list = get_countries_by_region(region)
            return jsonify({
                "type": "region",
                "region": region,
                "count": len(countries_list),
                "countries": countries_list
            })
        else:
            # Get all countries
            all_countries = get_all_countries()
            return jsonify({
                "type": "all",
                "count": len(all_countries),
                "countries": all_countries
            })
    except Exception as e:
        return jsonify({
            "error": f"Failed to fetch countries: {str(e)}"
        }), 500


@app.route("/countries/search", methods=["GET"])
def search_countries():
    """Search countries by name (alphabetic)"""
    query = request.args.get("q", "").strip()
    
    if not query or len(query) == 0:
        return jsonify({
            "error": "Query parameter 'q' is required",
            "example": "/countries/search?q=a"
        }), 400
    
    try:
        suggestions = get_country_suggestions(query)
        return jsonify({
            "query": query,
            "count": len(suggestions),
            "results": suggestions
        })
    except Exception as e:
        return jsonify({
            "error": f"Failed to search countries: {str(e)}"
        }), 500


@app.route("/countries/regions", methods=["GET"])
def get_regions():
    """Get available regions"""
    try:
        all_countries = get_all_countries()
        regions = list(set([c.get("region", "") for c in all_countries if c.get("region")]))
        regions.sort()
        
        return jsonify({
            "count": len(regions),
            "regions": regions
        })
    except Exception as e:
        return jsonify({
            "error": f"Failed to fetch regions: {str(e)}"
        }), 500


@app.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user, err = create_user(email, password)
    if err:
        return jsonify({"error": err}), 400

    token = create_token_for_user(user)
    return jsonify({"message": "user registered", "token": token, "email": user.email}), 201


@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = get_user_by_email(email)
    if not user or not verify_password(password, user.password_hash):
        return jsonify({"error": "invalid credentials"}), 401

    token = create_token_for_user(user)
    return jsonify({"message": "logged in", "token": token, "email": user.email})


@app.route("/auth/google", methods=["GET"])
def auth_google():
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        return jsonify({
            "error": "Google OAuth not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET."
        }), 500

    state = secrets.token_urlsafe(24)
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
    resp = make_response(redirect(auth_url))
    resp.set_cookie("gt_oauth_state", state, httponly=True, samesite="Lax")
    return resp


@app.route("/auth/google/callback", methods=["GET"])
def auth_google_callback():
    error = request.args.get("error")
    if error:
        return redirect(f"{FRONTEND_URL.rstrip('/')}/?error={error}")

    code = request.args.get("code")
    state = request.args.get("state")
    expected_state = request.cookies.get("gt_oauth_state")
    if not code or not state or state != expected_state:
        return redirect(f"{FRONTEND_URL.rstrip('/')}/?error=invalid_oauth_state")

    token_res = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
        timeout=10,
    )
    if token_res.status_code != 200:
        return redirect(f"{FRONTEND_URL.rstrip('/')}/?error=google_token_exchange_failed")

    token_data = token_res.json()
    access_token = token_data.get("access_token")
    if not access_token:
        return redirect(f"{FRONTEND_URL.rstrip('/')}/?error=missing_access_token")

    userinfo_res = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    if userinfo_res.status_code != 200:
        return redirect(f"{FRONTEND_URL.rstrip('/')}/?error=google_userinfo_failed")

    userinfo = userinfo_res.json()
    email = userinfo.get("email")
    if not email:
        return redirect(f"{FRONTEND_URL.rstrip('/')}/?error=email_not_available")

    user = get_user_by_email(email)
    if not user:
        random_pw = secrets.token_urlsafe(18)
        user, err = create_user(email, random_pw)
        if err:
            return redirect(f"{FRONTEND_URL.rstrip('/')}/?error=user_create_failed")

    token = create_token_for_user(user)
    return redirect(f"{FRONTEND_URL.rstrip('/')}/?token={token}")


@app.route("/auth/me", methods=["GET"])
def me():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "Authorization header required"}), 401

    token = auth.split(" ", 1)[1]
    payload = decode_token(token)
    if not payload:
        return jsonify({"error": "invalid or expired token"}), 401

    email = payload.get("sub")
    user = get_user_by_email(email)
    if not user:
        return jsonify({"error": "user not found"}), 404

    return jsonify({"email": user.email, "created_at": user.created_at.isoformat()})


@app.route("/countries/<region>", methods=["GET"])
def countries_by_region(region):
    """Get countries by region"""
    try:
        countries_list = get_countries_by_region(region)
        return jsonify({
            "region": region,
            "count": len(countries_list),
            "countries": countries_list
        })
    except Exception as e:
        return jsonify({
            "error": f"Failed to fetch countries for region: {str(e)}"
        }), 500


# ============== CITIES ENDPOINTS ==============

@app.route("/cities", methods=["GET"])
def cities():
    """
    Get city suggestions or all cities
    Query parameters:
    - search: Filter cities by name (starting with letter/text) - ALPHABETIC
    - region: Filter by region
    - country: Filter by country
    """
    search = request.args.get("search", "").strip()
    region = request.args.get("region", "").strip()
    country = request.args.get("country", "").strip()
    
    try:
        if search:
            # Get suggestions based on alphabetic search text
            suggestions = get_city_suggestions(search)
            return jsonify({
                "type": "suggestions",
                "search": search,
                "count": len(suggestions),
                "cities": suggestions
            })
        elif region:
            # Get cities by region
            cities_list = get_cities_by_region(region)
            return jsonify({
                "type": "region",
                "region": region,
                "count": len(cities_list),
                "cities": cities_list
            })
        elif country:
            # Get cities by country
            cities_list = get_cities_by_country(country)
            return jsonify({
                "type": "country",
                "country": country,
                "count": len(cities_list),
                "cities": cities_list
            })
        else:
            # Get all cities
            all_cities = get_all_cities()
            return jsonify({
                "type": "all",
                "count": len(all_cities),
                "cities": all_cities
            })
    except Exception as e:
        return jsonify({
            "error": f"Failed to fetch cities: {str(e)}"
        }), 500


@app.route("/cities/search", methods=["GET"])
def search_cities():
    """
    Search cities by alphabetic characters
    Example: /cities/search?q=lon → London
             /cities/search?q=new → New York
             /cities/search?q=s → Seoul, Shanghai, Singapore, Stockholm, São Paulo, Sydney
    """
    query = request.args.get("q", "").strip()
    
    if not query or len(query) == 0:
        return jsonify({
            "error": "Query parameter 'q' is required",
            "example": "/cities/search?q=l",
            "description": "Search for cities starting with the given letter(s)"
        }), 400
    
    try:
        suggestions = get_city_suggestions(query)
        return jsonify({
            "query": query,
            "count": len(suggestions),
            "results": suggestions
        })
    except Exception as e:
        return jsonify({
            "error": f"Failed to search cities: {str(e)}"
        }), 500


@app.route("/cities/regions", methods=["GET"])
def get_city_regions():
    """Get available regions for cities"""
    try:
        regions = get_available_regions()
        return jsonify({
            "count": len(regions),
            "regions": regions
        })
    except Exception as e:
        return jsonify({
            "error": f"Failed to fetch regions: {str(e)}"
        }), 500


@app.route("/cities/countries", methods=["GET"])
def get_city_countries():
    """Get available countries for cities"""
    try:
        countries = get_available_countries()
        return jsonify({
            "count": len(countries),
            "countries": countries
        })
    except Exception as e:
        return jsonify({
            "error": f"Failed to fetch countries: {str(e)}"
        }), 500


@app.route("/cities/<region>", methods=["GET"])
def cities_by_region(region):
    """Get cities by region"""
    try:
        cities_list = get_cities_by_region(region)
        return jsonify({
            "region": region,
            "count": len(cities_list),
            "cities": cities_list
        })
    except Exception as e:
        return jsonify({
            "error": f"Failed to fetch cities for region: {str(e)}"
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": {
            "all_events": "GET /events?city=<city>&source=all",
            "ticketmaster": "GET /events/ticketmaster?city=<city>",
            "bookmyshow": "GET /events/bookmyshow?city=<city>",
            "predicthq": "GET /events/predicthq?city=<city>",
            "by_source": "GET /events?city=<city>&source=<source>",
            "sources": "GET /sources",
            "health": "GET /health"
        }
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "message": str(error)
    }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
