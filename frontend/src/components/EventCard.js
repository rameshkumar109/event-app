import React from "react";
import "./EventCard.css";

function EventCard({ event }) {
  const getSourceInfo = (source) => {
    switch(source) {
      case "BookMyShow":
        return { emoji: "🎬", color: "#FF6B35" };
      case "PredictHQ":
        return { emoji: "🌍", color: "#00A651" };
      default: // Ticketmaster
        return { emoji: "🎭", color: "#FF0000" };
    }
  };

  const sourceInfo = getSourceInfo(event.source);
  
  return (
    <div className="event-card">
      <img src={event.image} alt={event.name} className="event-image" />
      <div className="event-content">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start", marginBottom: "10px" }}>
          <h3 className="event-title">{event.name}</h3>
          <span style={{ 
            fontSize: "0.75rem", 
            background: sourceInfo.color,
            color: "white",
            padding: "4px 8px",
            borderRadius: "4px",
            whiteSpace: "nowrap",
            marginLeft: "8px"
          }}>
            {sourceInfo.emoji} {event.source}
          </span>
        </div>
        <div className="event-details">
          <div className="event-detail-item">
            <span className="event-detail-label">📅 Date:</span>
            <span className="event-detail-value">{event.date}</span>
          </div>
          <div className="event-detail-item">
            <span className="event-detail-label">🕐 Time:</span>
            <span className="event-detail-value">{event.time}</span>
          </div>
          <div className="event-detail-item">
            <span className="event-detail-label">📍 Venue:</span>
            <span className="event-detail-value">{event.venue}</span>
          </div>
        </div>
        <a href={event.url} target="_blank" rel="noreferrer" className="event-button">
          🎫 Get Tickets
        </a>
      </div>
    </div>
  );
}

export default EventCard;
