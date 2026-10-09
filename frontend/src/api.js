import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const getStats = () => API.get("/api/dashboard/stats");
export const getDevices = () => API.get("/api/devices");
export const getEvents = () => API.get("/api/events");
export const getAlerts = () => API.get("/api/alerts");

export default API;