import React, { useEffect, useMemo, useState } from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "../lib/api";
import { Icon } from "../App";

export default function RiskIndicator() {
  const [baseline, setBaseline] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setLoading(true);
    setError("");
    try {
      const [b, r] = await Promise.all([api.baseline(), api.results(20)]);
      setBaseline(b);
      setResults(r);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  const chartData = useMemo(() => {
    const counts = {};
    results.forEach((r) => {
      counts[r.scenario] = (counts[r.scenario] || 0) + 1;
    });
    return Object.entries(counts).map(([name, value]) => ({
      name: name.replaceAll("_", " "),
      events: value
    }));
  }, [results]);

  const threats = results.filter(r => r.decision === "THREAT DETECTED").length;
  const normal = results.filter(r => r.decision === "NORMAL").length;

  return (
    <section className="console-page page-width">
      <div className="console-header">
        <div>
          <span className="section-kicker">RISK INDICATOR / 01</span>
          <h1>Security telemetry.</h1>
          <p>Calibrated baseline, detection events and the current state of the prototype.</p>
        </div>
        <button className="button button-ghost" onClick={load} disabled={loading}>
          <Icon name="activity" size={16} /> {loading ? "Refreshing..." : "Refresh data"}
        </button>
      </div>

      {error && (
        <div className="notice notice-error">
          <Icon name="alert" size={17} />
          <div><strong>Backend unavailable</strong><span>{error}</span></div>
        </div>
      )}

      <div className="metric-grid">
        <Metric label="Baseline threshold" value={baseline ? `${baseline.threshold_percent.toFixed(3)}%` : "—"} note="3σ calibrated boundary" />
        <Metric label="Baseline mean" value={baseline ? `${baseline.mean_deviation_percent.toFixed(3)}%` : "—"} note="Expected deviation" />
        <Metric label="Threat events" value={threats} note="Logged detections" alert />
        <Metric label="Normal events" value={normal} note="Logged verifications" />
      </div>

      <div className="dashboard-grid">
        <section className="panel chart-panel">
          <div className="panel-head">
            <div><span className="panel-kicker">EVENT DISTRIBUTION</span><h2>Detection history</h2></div>
            <span className="live-tag">SQLITE LOG</span>
          </div>
          <div className="chart-wrap">
            {chartData.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 10, right: 15, left: -15, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="2 4" stroke="rgba(255,255,255,.07)" vertical={false} />
                  <XAxis dataKey="name" tick={{ fill: "#7f8b9d", fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis allowDecimals={false} tick={{ fill: "#7f8b9d", fontSize: 11 }} axisLine={false} tickLine={false} />
                  <Tooltip
                    contentStyle={{ background: "#0d1219", border: "1px solid #24303e", borderRadius: 8, color: "#f4f7fb" }}
                    cursor={{ fill: "rgba(255,255,255,.03)" }}
                  />
                  <Bar dataKey="events" fill="#8bd8ff" radius={[4,4,0,0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="empty-state">No logged events yet.</div>
            )}
          </div>
        </section>

        <section className="panel baseline-panel">
          <div className="panel-head">
            <div><span className="panel-kicker">CALIBRATION</span><h2>Quantum baseline</h2></div>
          </div>
          {baseline ? (
            <div className="baseline-list">
              <Row label="Repetitions" value={baseline.repetitions} />
              <Row label="Shots / run" value={baseline.shots_per_run.toLocaleString()} />
              <Row label="Noise probability" value={baseline.noise_probability} />
              <Row label="Mean deviation" value={`${baseline.mean_deviation_percent.toFixed(4)}%`} />
              <Row label="Std. deviation" value={`${baseline.std_deviation_percent.toFixed(4)}%`} />
              <Row label="Detection threshold" value={`${baseline.threshold_percent.toFixed(4)}%`} strong />
            </div>
          ) : (
            <div className="empty-state">Calibrate the backend before viewing the baseline.</div>
          )}
        </section>
      </div>

      <section className="panel event-panel">
        <div className="panel-head">
          <div><span className="panel-kicker">RECENT ACTIVITY</span><h2>Detection log</h2></div>
        </div>
        {results.length ? (
          <div className="event-table">
            <div className="event-row event-head"><span>SCENARIO</span><span>DECISION</span><span>RISK</span><span>TIME</span></div>
            {results.map((r) => (
              <div className="event-row" key={r.id}>
                <span className="scenario-name">{r.scenario.replaceAll("_", " ")}</span>
                <span className={`decision ${r.decision === "THREAT DETECTED" ? "danger" : "safe"}`}>
                  <i />{r.decision}
                </span>
                <span className="risk-value">{r.risk_score}</span>
                <span className="time-value">{new Date(r.timestamp).toLocaleTimeString()}</span>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">No results logged yet. Run a verification from the prototype console.</div>
        )}
      </section>
    </section>
  );
}

function Metric({ label, value, note, alert }) {
  return (
    <div className={`metric-card ${alert ? "metric-alert" : ""}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{note}</small>
    </div>
  );
}

function Row({ label, value, strong }) {
  return <div className="baseline-row"><span>{label}</span><strong className={strong ? "accent-value" : ""}>{value}</strong></div>;
}
