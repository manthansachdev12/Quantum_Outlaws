import React, { useState } from "react";
import { api } from "../lib/api";
import { Icon } from "../App";

const attackCards = [
  { key: "forgery", title: "Forgery", desc: "Alter the signed payload and verify signature integrity." },
  { key: "impersonation", title: "Impersonation", desc: "Present a signature under an unauthorized identity." },
  { key: "replay", title: "Replay", desc: "Reuse a previously observed signature identifier." },
  { key: "channel", title: "Channel manipulation", desc: "Inject stronger quantum-channel noise and compare it with the baseline." }
];

export default function Prototype() {
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function run(label, action) {
    setBusy(true);
    setError("");
    try {
      const data = await action();
      setResult({ ...data, label });
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="console-page page-width">
      <div className="console-header">
        <div>
          <span className="section-kicker">PROTOTYPE / 02</span>
          <h1>Security console.</h1>
          <p>Execute controlled verification and attack simulations against the FastAPI detection layer.</p>
        </div>
        <div className="console-badge"><span className="status-dot online" /> LIVE SIMULATION</div>
      </div>

      {error && <div className="notice notice-error"><Icon name="alert" size={17} /><div><strong>Request failed</strong><span>{error}</span></div></div>}

      <div className="prototype-layout">
        <div className="control-column">
          <section className="panel">
            <div className="panel-head">
              <div><span className="panel-kicker">BASELINE VERIFICATION</span><h2>Run normal verification</h2></div>
              <span className="method-tag">BELL / Φ+</span>
            </div>
            <p className="panel-description">
              Measure the Bell state under the calibrated noise condition. The
              observed deviation is compared with the persistent baseline.
            </p>
            <div className="form-grid">
              <label><span>Shots</span><input type="number" defaultValue="4096" id="verify-shots" /></label>
              <label><span>Noise probability</span><input type="number" step="0.001" defaultValue="0.01" id="verify-noise" /></label>
            </div>
            <button className="button button-primary full" disabled={busy} onClick={() => {
              const shots = Number(document.getElementById("verify-shots").value);
              const noise_probability = Number(document.getElementById("verify-noise").value);
              run("Normal verification", () => api.verify({ shots, noise_probability }));
            }}>
              {busy ? "Running quantum simulation..." : "Run verification"} <Icon name="arrow" size={16} />
            </button>
          </section>

          <section className="panel attack-panel">
            <div className="panel-head">
              <div><span className="panel-kicker">CONTROLLED ATTACKS</span><h2>Test the detector</h2></div>
            </div>
            <div className="attack-list">
              {attackCards.map((attack, index) => (
                <button className="attack-item" key={attack.key} disabled={busy} onClick={() => {
                  if (attack.key === "forgery") {
                    run("Forgery", () => api.forgery({
                      original_signature: "Alice-Signature-001",
                      modified_signature: "Alice-Signature-999"
                    }));
                  }
                  if (attack.key === "impersonation") {
                    run("Impersonation", () => api.impersonation({
                      expected_signer: "Alice",
                      presented_signer: "Eve"
                    }));
                  }
                  if (attack.key === "replay") {
                    run("Replay", () => api.replay({ signature_id: "SIG-UI-001" }));
                  }
                  if (attack.key === "channel") {
                    run("Channel manipulation", () => api.channel({
                      shots: 4096,
                      noise_probability: 0.08,
                      likelihood_threshold: 10
                    }));
                  }
                }}>
                  <span className="attack-index">0{index + 1}</span>
                  <span className="attack-copy"><strong>{attack.title}</strong><small>{attack.desc}</small></span>
                  <Icon name="arrow" size={16} />
                </button>
              ))}
            </div>
            <p className="prototype-note">
              Replay detection is stateful. The first submission of <code>SIG-UI-001</code>
              is treated as new; repeating it triggers the replay rule.
            </p>
          </section>
        </div>

        <section className="panel result-panel">
          <div className="panel-head">
            <div><span className="panel-kicker">DETECTION OUTPUT</span><h2>Evidence</h2></div>
            {result && <span className={`result-state ${isThreat(result) ? "danger" : "safe"}`}>
              {isThreat(result) ? "THREAT" : "NORMAL"}
            </span>}
          </div>

          {!result ? (
            <div className="result-empty">
              <div className="empty-orbit"><span /></div>
              <strong>Awaiting a test</strong>
              <p>Run a verification or controlled attack to inspect the detector's evidence.</p>
            </div>
          ) : (
            <ResultView result={result} />
          )}
        </section>
      </div>
    </section>
  );
}

function isThreat(result) {
  return result.decision === "THREAT DETECTED" || result.detected === true;
}

function ResultView({ result }) {
  const threat = isThreat(result);
  const isQuantumResult = Boolean(
    result.counts ||
    result.observed_deviation_percent != null ||
    result.threshold_percent != null ||
    result.likelihood_ratio != null
  );

  return (
    <div className="result-content">
      <div className={`result-banner ${threat ? "threat" : "normal"}`}>
        <span className="result-icon"><Icon name={threat ? "alert" : "check"} size={20} /></span>
        <div>
          <strong>{threat ? "Threat detected" : "Verification normal"}</strong>
          <span>{result.reason || getDefaultReason(result)}</span>
        </div>
      </div>

      {isQuantumResult ? (
        <QuantumEvidence result={result} />
      ) : (
        <AttackEvidence result={result} />
      )}

      <div className="result-id">RUN ID <code>{result.result_id || "local"}</code></div>
    </div>
  );
}

function AttackEvidence({ result }) {
  const attack = result.attack || result.label || "attack";
  const rows = [
    ["Attack type", pretty(attack)],
    ["Detection", result.detected ? "THREAT DETECTED" : "NOT DETECTED"],
    ["Severity", result.severity || "—"],
    ["Risk indicator", result.risk_score ?? "—"],
    ["Reason", result.reason || "—"]
  ];

  return (
    <>
      <div className="attack-evidence">
        {rows.map(([label, value]) => (
          <div className="attack-evidence-row" key={label}>
            <span>{label}</span>
            <strong className={
              label === "Detection" && result.detected ? "danger-text" :
              label === "Severity" && result.severity === "HIGH" ? "danger-text" :
              label === "Risk indicator" && Number(result.risk_score) >= 70 ? "danger-text" : ""
            }>
              {value}
            </strong>
          </div>
        ))}
      </div>

      {result.attack === "impersonation" && (
        <div className="evidence-detail">
          <span>IDENTITY CHECK</span>
          <div><strong>Expected signer</strong><b>Alice</b></div>
          <div><strong>Presented signer</strong><b>Eve</b></div>
        </div>
      )}

      {result.attack === "forgery" && (
        <div className="evidence-detail">
          <span>INTEGRITY CHECK</span>
          <div><strong>Original</strong><b>Alice-Signature-001</b></div>
          <div><strong>Modified</strong><b>Alice-Signature-999</b></div>
        </div>
      )}

      {result.attack === "replay" && (
        <div className="evidence-detail">
          <span>REPLAY GUARD</span>
          <div><strong>Signature ID</strong><b>SIG-UI-001</b></div>
          <div><strong>State</strong><b>{result.detected ? "Previously observed" : "New signature"}</b></div>
        </div>
      )}
    </>
  );
}

function QuantumEvidence({ result }) {
  const metrics = [
    ["Scenario", pretty(result.attack || result.scenario || "verification")],
    ["Decision", result.decision || (result.detected ? "THREAT DETECTED" : "NORMAL")],
    ["Risk indicator", result.risk_score ?? "—"],
    ["Observed deviation", result.observed_deviation_percent != null ? `${result.observed_deviation_percent.toFixed(4)}%` : "—"],
    ["Threshold", result.threshold_percent != null ? `${result.threshold_percent.toFixed(4)}%` : "—"],
    ["Likelihood ratio", result.likelihood_ratio != null ? formatRatio(result.likelihood_ratio) : "—"]
  ];

  return (
    <>
      <div className="result-metrics">
        {metrics.map(([label, value]) => (
          <div className="result-metric" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>

      {result.counts && (
        <div className="measurement-box">
          <div className="measurement-head">
            <span>MEASUREMENT OUTCOMES</span>
            <span>{result.shots?.toLocaleString()} SHOTS</span>
          </div>
          <div className="measurement-bars">
            {["00", "01", "10", "11"].map((key) => {
              const count = result.counts[key] || 0;
              const pct = result.shots ? (count / result.shots) * 100 : 0;
              return (
                <div className="measurement-row" key={key}>
                  <span>|{key}⟩</span>
                  <div className="bar-track"><i style={{ width: `${Math.min(pct * 2, 100)}%` }} /></div>
                  <strong>{pct.toFixed(2)}%</strong>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </>
  );
}

function getDefaultReason(result) {
  if (result.attack === "forgery") return "Signature integrity mismatch.";
  if (result.attack === "impersonation") return "Signer identity mismatch.";
  if (result.attack === "replay") return "Signature ID was previously observed.";
  return "The observation remained within the configured detection rules.";
}

function pretty(value) {
  return String(value)
    .replaceAll("_", " ")
    .replace(/\b\w/g, c => c.toUpperCase());
}

function formatRatio(value) {
  if (value === 0) return "0";
  if (Math.abs(value) >= 1000) return value.toExponential(3);
  return Number(value).toFixed(3);
}
