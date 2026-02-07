import requests
from flask import jsonify

def get_countries():
    """
    Fetch all countries from REST Countries API
    """
    try:
        response = requests.get("https://restcountries.com/v3.1/all", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error fetching countries: {e}")
        return []


def get_country_suggestions(search_text):
    """
    Get country suggestions based on search text
    Returns matching countries sorted alphabetically
    """
    try:
        countries = get_countries()
        
        if not countries:
            return []
        
        search_lower = search_text.lower().strip()
        
        if len(search_lower) == 0:
            return []
        
        suggestions = []
        
        for country in countries:
            # Check country name
            country_name = country.get("name", {}).get("common", "")
            
            # Check common name
            if country_name.lower().startswith(search_lower):
                suggestions.append({
                    "name": country_name,
                    "code": country.get("cca2", ""),
                    "flag": country.get("flag", "🌍"),
                    "region": country.get("region", ""),
                    "capital": country.get("capital", [""])[0] if country.get("capital") else ""
                })
            # Also check official name
            else:
                official_name = country.get("name", {}).get("official", "")
                if official_name.lower().startswith(search_lower):
                    suggestions.append({
                        "name": country_name,
                        "code": country.get("cca2", ""),
                        "flag": country.get("flag", "🌍"),
                        "region": country.get("region", ""),
                        "capital": country.get("capital", [""])[0] if country.get("capital") else ""
                    })
        
        # Sort alphabetically by name
        suggestions.sort(key=lambda x: x["name"])
        
        return suggestions[:10]  # Return top 10 matches
    
    except Exception as e:
        print(f"Error getting country suggestions: {e}")
        return []


def get_all_countries():
    """
    Get all countries sorted alphabetically
    """
    try:
        countries = get_countries()
        
        if not countries:
            return []
        
        result = []
        for country in countries:
            country_name = country.get("name", {}).get("common", "")
            result.append({
                "name": country_name,
                "code": country.get("cca2", ""),
                "flag": country.get("flag", "🌍"),
                "region": country.get("region", ""),
                "subregion": country.get("subregion", ""),
                "capital": country.get("capital", [""])[0] if country.get("capital") else "",
                "population": country.get("population", 0)
            })
        
        # Sort alphabetically by name
        result.sort(key=lambda x: x["name"])
        
        return result
    
    except Exception as e:
        print(f"Error getting all countries: {e}")
        return []


def get_countries_by_region(region):
    """
    Get countries filtered by region
    """
    try:
        countries = get_countries()
        
        if not countries:
            return []
        
        region_lower = region.lower()
        result = []
        
        for country in countries:
            if country.get("region", "").lower() == region_lower:
                country_name = country.get("name", {}).get("common", "")
                result.append({
                    "name": country_name,
                    "code": country.get("cca2", ""),
                    "flag": country.get("flag", "🌍"),
                    "region": country.get("region", ""),
                    "capital": country.get("capital", [""])[0] if country.get("capital") else "",
                    "population": country.get("population", 0)
                })
        
        # Sort alphabetically by name
        result.sort(key=lambda x: x["name"])
        
        return result
    
    except Exception as e:
        print(f"Error getting countries by region: {e}")
        return []
