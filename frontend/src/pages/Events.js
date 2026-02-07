import React, { useState } from "react";
import SearchBar from "../components/SearchBar";
import EventList from "../components/EventList";
import { getEventsByCity } from "../services/api";
import "./Events.css";

export default function Events() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem("gt_user_token");
    window.location.href = "/";
  };

  const searchEvents = async (cityName) => {
    setLoading(true);

    try {
      const response = await getEventsByCity(cityName);
      setEvents(response.data.events);
    } catch (error) {
      alert("Error fetching events");
    }

    setLoading(false);
  };

  return (
    <div className="app-container">
      <header className="events-topbar">
        <div className="events-brand">
          <span className="events-brand-dot" />
          GloboTicket
        </div>
        <button className="events-logout" type="button" onClick={handleLogout}>
          Log out
        </button>
      </header>

      <div className="app-header">
        <h1>🎫 GloboTicket</h1>
        <p>Discover amazing events near you</p>
      </div>

      <div className="search-container">
        <SearchBar onSearch={searchEvents} />
      </div>

      {loading && <div className="loading-message">⏳ Loading events...</div>}

      {!loading && <EventList events={events} />}
    </div>
  );
}
