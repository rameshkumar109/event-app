import React, { useState } from "react";
import EventCard from "./EventCard";
import "./EventList.css";

function EventList({ events }) {
  const [selectedSource, setSelectedSource] = useState("all");

  // Filter events by source
  const filteredEvents = selectedSource === "all"
    ? events
    : events.filter(event => event.source === selectedSource);

  // Get unique sources
  const sources = ["all", ...new Set(events.map(e => e.source))];

  const getSourceLabel = (source) => {
    switch(source) {
      case "BookMyShow":
        return "🎬 BookMyShow";
      case "PredictHQ":
        return "🌍 PredictHQ";
      case "Ticketmaster":
        return "🎭 Ticketmaster";
      default:
        return "🎪 All Events";
    }
  };

  if (!events.length)
    return (
      <div className="no-events-container">
        <p className="no-events-message">🔍 Search for a city to discover amazing events</p>
      </div>
    );

  return (
    <div>
      {sources.length > 1 && (
        <div className="source-filter">
          {sources.map((source) => (
            <button
              key={source}
              className={`source-filter-button ${selectedSource === source ? "active" : ""}`}
              onClick={() => setSelectedSource(source)}
            >
              {getSourceLabel(source)}
            </button>
          ))}
        </div>
      )}

      {filteredEvents.length > 0 ? (
        <div className="events-list-container">
          {filteredEvents.map(event => (
            <EventCard key={event.id} event={event} />
          ))}
        </div>
      ) : (
        <div className="no-events-container">
          <p className="no-events-message">📭 No events found from {selectedSource}</p>
        </div>
      )}
    </div>
  );
}

export default EventList;
