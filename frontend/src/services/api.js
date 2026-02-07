import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

// Get events from all sources (Ticketmaster + BookMyShow + PredictHQ)
export const getEventsByCity = (city) => {
  return API.get(`/events?city=${city}&source=all`);
};

// Get events only from Ticketmaster
export const getEventsByCity_Ticketmaster = (city) => {
  return API.get(`/events/ticketmaster?city=${city}`);
};

// Get events only from BookMyShow
export const getEventsByCity_BookMyShow = (city) => {
  return API.get(`/events/bookmyshow?city=${city}`);
};

// Get events only from PredictHQ
export const getEventsByCity_PredictHQ = (city) => {
  return API.get(`/events/predicthq?city=${city}`);
};

// Get events from specific source
export const getEventsByCity_Source = (city, source) => {
  return API.get(`/events?city=${city}&source=${source}`);
};

