import React, { useState } from "react";
import "./SearchBar.css";

function SearchBar({ onSearch }) {
  const [city, setCity] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestions, setSuggestions] = useState([]);

  const API_BASE = "http://127.0.0.1:5000";

  // Fetch city suggestions as user types (alphabetic search)
  const fetchCitySuggestions = async (searchText) => {
    if (!searchText.trim() || searchText.length < 1) {
      setSuggestions([]);
      return;
    }

    try {
  const url = `${API_BASE}/cities/search?q=${encodeURIComponent(searchText)}`;
  console.debug("Fetching city suggestions from:", url);
  const response = await fetch(url);
  const data = await response.json();
  console.debug("/cities/search response:", data);

  // Accept either `results` or `cities` in response
  const list = data.results || data.cities || [];
  setSuggestions(Array.isArray(list) ? list : []);
    } catch (error) {
      console.error("Error fetching city suggestions:", error);
      setSuggestions([]);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!city.trim()) return;
    onSearch(city);
    setShowSuggestions(false);
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setCity(value);
    if (value.length >= 1) {
      fetchCitySuggestions(value);
      setShowSuggestions(true);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  };

  const handleSelectCity = (cityName) => {
    setCity(cityName);
    onSearch(cityName);
    setShowSuggestions(false);
  };

  return (
    <div className="suggestions-container">
      <form onSubmit={handleSubmit} className="search-form">
        <div className="search-input-wrapper">
          <input
            type="text"
            placeholder="Search events by city..."
            value={city}
            onChange={handleInputChange}
            onFocus={() => city.length > 0 && setShowSuggestions(true)}
            onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
            className="search-input"
          />
          {showSuggestions && suggestions.length > 0 && (
            <div className="suggestions-dropdown">
              {suggestions.map((suggestion, index) => (
                <div
                  key={index}
                  className="suggestion-item"
                  onMouseDown={() => handleSelectCity(suggestion.name)}
                >
                  <span className="suggestion-emoji">{suggestion.emoji}</span>
                  <div className="suggestion-text">
                    <div className="suggestion-name">{suggestion.name}</div>
                    <div className="suggestion-country">{suggestion.country}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
        <button type="submit" className="search-button">
          Search
        </button>
      </form>

    </div>
  );
}

export default SearchBar;
