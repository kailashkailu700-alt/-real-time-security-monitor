import { useEffect, useState } from "react";
import { getStats, getDevices, getEvents, getAlerts } from "./api";
import "./App.css";

function App() {
  const [stats, setStats] = useState(null);
  const [devices, setDevices] = useState([]);
  const [events, setEvents] = useState([]);
  const [alerts, setAlerts] = useState([]);

  const loadData = async () => {
    try {
      const [s, d, e, a] = await Promise.all([
        getStats(),
        getDevices(),
        getEvents(),
        getAlerts(),
      ]);
      setStats(s.data);
      setDevices(d.data);
      setEvents(e.data);
      setAlerts(a.data);
    } catch (err) {
      console.error("Load error:", err);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  const riskColor = (level) => {
    if (level === "CRITICAL") return "#dc2626";
    if (level === "HIGH") return "#f97316";
    if (level === "MEDIUM") return "#eab308";
    return "#22c55e";
  };

  return (
    <div className="container">
      <header>
        <h1>🛡️ Real-Time Security Monitor</h1>
        <p>External Device Intrusion Detection System</p>
      </header>

      {/* Stats Cards */}
      {stats && (
        <div className="stats-grid">
          <div className="card">
            <h3>Devices</h3>
            <p className="big">{stats.devices.total}</p>
            <small>Online: {stats.devices.online} | Offline: {stats.devices.offline}</small>
          </div>
          <div className="card">
            <h3>Events</h3>
            <p className="big">{stats.events.total}</p>
            <small>Total security events</small>
          </div>
          <div className="card">
            <h3>Alerts</h3>
            <p className="big">{stats.alerts.total}</p>
            <small>Open: {stats.alerts.open}</small>
          </div>
          <div className="card">
            <h3>Risk Levels</h3>
            <div className="risk-list">
              <span style={{ color: riskColor("CRITICAL") }}>
                C: {stats.alerts.by_risk.CRITICAL}
              </span>
              <span style={{ color: riskColor("HIGH") }}>
                H: {stats.alerts.by_risk.HIGH}
              </span>
              <span style={{ color: riskColor("MEDIUM") }}>
                M: {stats.alerts.by_risk.MEDIUM}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Devices */}
      <section>
        <h2>💻 Monitored Devices</h2>
        <table>
          <thead>
            <tr>
              <th>Device ID</th>
              <th>Hostname</th>
              <th>IP</th>
              <th>OS</th>
              <th>Status</th>
              <th>Last Seen</th>
            </tr>
          </thead>
          <tbody>
            {devices.map((d) => (
              <tr key={d.id}>
                <td>{d.device_id}</td>
                <td>{d.hostname}</td>
                <td>{d.ip_address}</td>
                <td>{d.operating_system}</td>
                <td>
                  <span className={`badge ${d.status}`}>{d.status}</span>
                </td>
                <td>{new Date(d.last_seen).toLocaleTimeString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {/* Alerts */}
      <section>
        <h2>🚨 Active Alerts</h2>
        {alerts.length === 0 ? (
          <p className="empty">No alerts</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Risk</th>
                <th>Type</th>
                <th>Device</th>
                <th>Message</th>
                <th>Status</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map((a) => (
                <tr key={a.id}>
                  <td>
                    <span
                      className="badge"
                      style={{ background: riskColor(a.risk_level) }}
                    >
                      {a.risk_level}
                    </span>
                  </td>
                  <td>{a.alert_type}</td>
                  <td>{a.device_id}</td>
                  <td>{a.message}</td>
                  <td>{a.status}</td>
                  <td>{new Date(a.created_at).toLocaleTimeString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      {/* Events */}
      <section>
        <h2>📊 Recent Security Events</h2>
        {events.length === 0 ? (
          <p className="empty">No events</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Type</th>
                <th>Source IP</th>
                <th>Port</th>
                <th>Severity</th>
                <th>Description</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {events.slice(0, 20).map((e) => (
                <tr key={e.id}>
                  <td>{e.event_type}</td>
                  <td>{e.source_ip || "-"}</td>
                  <td>{e.port || "-"}</td>
                  <td>
                    <span
                      className="badge"
                      style={{ background: riskColor(e.severity) }}
                    >
                      {e.severity}
                    </span>
                  </td>
                  <td>{e.description || "-"}</td>
                  <td>{new Date(e.timestamp).toLocaleTimeString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <footer>
        <small>Auto-refresh every 5 seconds · Last update: {new Date().toLocaleTimeString()}</small>
      </footer>
    </div>
  );
}

export default App;