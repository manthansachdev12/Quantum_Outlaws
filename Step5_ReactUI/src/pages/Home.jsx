import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Icon } from "../App";

const threats = [
  {
    number: "01",
    title: "Forgery",
    text: "A legitimate signature payload is altered after signing. The verification layer must expose the resulting integrity mismatch."
  },
  {
    number: "02",
    title: "Impersonation",
    text: "An unauthorized party presents a signature under another identity. The system checks the expected signer against the presented identity."
  },
  {
    number: "03",
    title: "Replay",
    text: "A previously accepted signature is submitted again. The prototype tracks signature identifiers and flags reuse."
  },
  {
    number: "04",
    title: "Channel manipulation",
    text: "The quantum communication path is disturbed. Measurement statistics are compared against a calibrated noise baseline."
  }
];

const principles = [
  ["Pauli eigenstates", "Quantum states provide structured measurement bases for verification."],
  ["Projective measurement", "Observed outcomes become measurable evidence instead of a black-box prediction."],
  ["Statistical thresholds", "Deviation from the calibrated baseline becomes a deterministic detection signal."],
  ["Hypothesis testing", "Chi-square and likelihood-ratio analysis quantify how unusual an observation is."]
];

export default function Home() {
  const [hoveredThreat, setHoveredThreat] = useState(null);
  const [hoveredProblem, setHoveredProblem] = useState(null);
  const [hoveredPrinciple, setHoveredPrinciple] = useState(null);
  const [hoveredPipeline, setHoveredPipeline] = useState(null);
  const [hoveredStack, setHoveredStack] = useState(null);
  const [hoveredNode, setHoveredNode] = useState(null);

  const cardStyle = {
    transition: "transform 0.15s ease, border-color 0.15s ease",
    cursor: "default"
  };

  return (
    <>
      <section className="hero page-width">
        <div className="hero-copy">
          <div className="eyebrow">
            <span className="eyebrow-line" /> SIH26141 · QUANTUM OUTLAWS
          </div>
          <h1>
            Threat detection for the <em>quantum signature era.</em>
          </h1>
          <p className="hero-lead">
            Q-SHIELD is a quantum-inspired security layer for teleportation-based
            Quantum Digital Signatures. It uses quantum measurement principles
            and statistical thresholds to identify anomalous verification events —
            without AI or machine learning.
          </p>
          <div className="hero-actions">
            <Link
              to="/prototype"
              className="button button-primary"
              style={{
                transition: "transform 0.15s ease, opacity 0.15s ease",
                display: "inline-flex",
                alignItems: "center"
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = "translateY(-1px)";
                e.currentTarget.style.opacity = "0.9";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = "translateY(0)";
                e.currentTarget.style.opacity = "1";
              }}
            >
              Open prototype <Icon name="arrow" size={17} />
            </Link>
            <Link
              to="/risk"
              className="button button-ghost"
              style={{
                transition: "transform 0.15s ease, background-color 0.15s ease"
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = "translateY(-1px)";
                e.currentTarget.style.backgroundColor = "rgba(255, 255, 255, 0.05)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = "translateY(0)";
                e.currentTarget.style.backgroundColor = "";
              }}
            >
              View risk indicator
            </Link>
          </div>
          <div className="hero-meta">
            <span><i /> No AI / ML</span>
            <span><i /> Deterministic rules</span>
            <span><i /> Statistical evidence</span>
          </div>
        </div>

        <div className="hero-visual" aria-label="Quantum security visualization">
          <div className="orbit orbit-a" />
          <div className="orbit orbit-b" />
          <div className="orbit orbit-c" />
          <div className="core">
            <span className="core-ring" />
            <span className="core-pulse" />
            <div className="core-label">
              <small>Q-CORE</small>
              <strong>01</strong>
              <span>VERIFICATION</span>
            </div>
          </div>
          <div
            className="signal-card signal-top"
            style={{
              transition: "transform 0.15s ease",
              cursor: "pointer"
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-2px)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
            }}
          >
            <span>MEASUREMENT</span>
            <strong>|Φ+⟩</strong>
          </div>
          <div
            className="signal-card signal-bottom"
            style={{
              transition: "transform 0.15s ease",
              cursor: "pointer"
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-2px)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
            }}
          >
            <span>DETECTION MODE</span>
            <strong>STATISTICAL</strong>
          </div>
        </div>
      </section>

      <section className="section section-dark">
        <div className="page-width">
          <div className="section-heading split">
            <div>
              <span className="section-kicker">01 / THE PROBLEM</span>
              <h2>The cryptographic transition creates a new detection gap.</h2>
            </div>
            <p>
              Quantum computing threatens classical public-key cryptography,
              while quantum digital signatures introduce a different security
              surface: the protocol can have strong security guarantees without
              necessarily having a dedicated operational threat-detection layer.
            </p>
          </div>

          <div className="problem-grid">
            {[
              {
                idx: "CONTEXT",
                title: "From classical signatures to quantum-secure verification",
                desc: "Shor's algorithm motivates the migration away from vulnerable RSA/ECC signatures. Teleportation-based QDS uses entanglement, measurement and quantum states to support information-theoretic security. The SIH problem asks for a detection framework that can observe anomalous behavior around that protocol.",
                main: true
              },
              {
                idx: "THE GAP",
                title: "Detection, not replacement.",
                desc: "The proposed layer is designed as a protocol-native detection component. It observes measurement behavior, checks explicit security conditions and raises an alert when evidence crosses configured statistical thresholds.",
                main: false
              },
              {
                idx: "CONSTRAINT",
                title: "Quantum principles only.",
                desc: "The solution deliberately avoids black-box AI/ML decisions. Its evidence comes from Pauli eigenstates, projective measurements, calibrated statistics and explicit threshold rules.",
                main: false
              }
            ].map((card, i) => (
              <article
                key={card.idx}
                className={`problem-card ${card.main ? "problem-main" : ""}`}
                style={{
                  ...cardStyle,
                  transform: hoveredProblem === i ? "translateY(-2px)" : "translateY(0)"
                }}
                onMouseEnter={() => setHoveredProblem(i)}
                onMouseLeave={() => setHoveredProblem(null)}
              >
                <div className="card-index">{card.idx}</div>
                <h3>{card.title}</h3>
                <p>{card.desc}</p>
                {card.main && (
                  <>
                    <div className="card-rule" />
                    <div className="mini-stat-row">
                      <div><strong>4</strong><span>attack classes</span></div>
                      <div><strong>0</strong><span>AI / ML models</span></div>
                      <div><strong>1</strong><span>calibrated baseline</span></div>
                    </div>
                  </>
                )}
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="page-width">
          <div className="section-heading">
            <span className="section-kicker">02 / THREAT SURFACE</span>
            <h2>Four attack paths. One detection layer.</h2>
            <p>
              The prototype maps the SIH threat categories into observable
              verification signals, combining protocol checks with quantum
              measurement statistics.
            </p>
          </div>

          <div className="threat-grid">
            {threats.map((item, index) => {
              const isHovered = hoveredThreat === index;
              return (
                <article
                  className="threat-card"
                  key={item.number}
                  style={{
                    ...cardStyle,
                    cursor: "pointer",
                    transform: isHovered ? "translateY(-2px)" : "translateY(0)"
                  }}
                  onMouseEnter={() => setHoveredThreat(index)}
                  onMouseLeave={() => setHoveredThreat(null)}
                >
                  <span className="threat-number">{item.number}</span>
                  <h3>{item.title}</h3>
                  <p>{item.text}</p>
                  <span
                    className="threat-link"
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      gap: isHovered ? "7px" : "4px",
                      transition: "gap 0.15s ease"
                    }}
                  >
                    DETECTION PATH <Icon name="arrow" size={14} />
                  </span>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section className="section section-dark">
        <div className="page-width">
          <div className="section-heading split">
            <div>
              <span className="section-kicker">03 / HOW IT WORKS</span>
              <h2>Evidence from the quantum layer.</h2>
            </div>
            <p>
              A calibrated baseline establishes expected measurement behavior.
              New observations are then compared against that baseline using
              deterministic statistical rules.
            </p>
          </div>

          <div className="principles">
            {principles.map(([title, text], index) => {
              const isHovered = hoveredPrinciple === index;
              return (
                <div
                  className="principle"
                  key={title}
                  style={{
                    transition: "transform 0.15s ease",
                    transform: isHovered ? "translateX(4px)" : "translateX(0)"
                  }}
                  onMouseEnter={() => setHoveredPrinciple(index)}
                  onMouseLeave={() => setHoveredPrinciple(null)}
                >
                  <span>0{index + 1}</span>
                  <div>
                    <h3>{title}</h3>
                    <p>{text}</p>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="pipeline">
            {[
              { num: "01", title: "Signature", sub: "Message + verification request" },
              { num: "02", title: "Quantum verification", sub: "Bell state + measurements" },
              { num: "03", title: "Analysis", sub: "Deviation + χ² + likelihood" },
              { num: "04", title: "Decision", sub: "Normal or threat detected" }
            ].map((step, idx) => {
              const isHovered = hoveredPipeline === idx;
              return (
                <React.Fragment key={step.num}>
                  {idx > 0 && <div className="pipeline-line" />}
                  <div
                    className="pipeline-step"
                    style={{
                      transition: "transform 0.15s ease",
                      transform: isHovered ? "translateY(-2px)" : "translateY(0)"
                    }}
                    onMouseEnter={() => setHoveredPipeline(idx)}
                    onMouseLeave={() => setHoveredPipeline(null)}
                  >
                    <span>{step.num}</span>
                    <strong>{step.title}</strong>
                    <small>{step.sub}</small>
                  </div>
                </React.Fragment>
              );
            })}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="page-width architecture">
          <div className="architecture-copy">
            <span className="section-kicker">04 / PROTOTYPE</span>
            <h2>Built to be demonstrated, measured and extended.</h2>
            <p>
              The current implementation runs as a controlled simulation using
              Qiskit Aer and exposes the detection engine through FastAPI.
              Results are persisted in SQLite and the React interface consumes
              the same API used by the prototype tests.
            </p>
            <div className="stack-list">
              {["React", "FastAPI", "Qiskit Aer", "NumPy / SciPy", "SQLite"].map((tool, idx) => (
                <span
                  key={tool}
                  style={{
                    display: "inline-block",
                    transition: "transform 0.15s ease",
                    transform: hoveredStack === idx ? "translateY(-1px)" : "translateY(0)",
                    cursor: "default"
                  }}
                  onMouseEnter={() => setHoveredStack(idx)}
                  onMouseLeave={() => setHoveredStack(null)}
                >
                  {tool}
                </span>
              ))}
            </div>
            <Link
              to="/prototype"
              className="text-link"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "6px",
                transition: "gap 0.15s ease"
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.gap = "8px";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.gap = "6px";
              }}
            >
              Enter the security console <Icon name="arrow" size={15} />
            </Link>
          </div>

          <div className="architecture-diagram">
            {[
              { title: "SIGNATURE", sub: "INPUT", active: false },
              { title: "QUANTUM", sub: "VERIFICATION", active: true },
              { title: "STATISTICAL", sub: "DETECTION", active: false },
              { title: "RISK", sub: "INDICATOR", active: false }
            ].map((node, i) => (
              <React.Fragment key={i}>
                {i > 0 && <div className="arch-connector" />}
                <div
                  className={`arch-node ${node.active ? "active" : ""}`}
                  style={{
                    transition: "transform 0.15s ease",
                    transform: hoveredNode === i ? "translateY(-2px)" : "translateY(0)"
                  }}
                  onMouseEnter={() => setHoveredNode(i)}
                  onMouseLeave={() => setHoveredNode(null)}
                >
                  {node.title}<br /><small>{node.sub}</small>
                </div>
              </React.Fragment>
            ))}
          </div>
        </div>
      </section>

      <section className="closing-cta">
        <div className="page-width cta-inner">
          <div>
            <span className="section-kicker">LIVE PROTOTYPE</span>
            <h2>See the detection layer in action.</h2>
          </div>
          <Link
            to="/prototype"
            className="button button-primary"
            style={{
              transition: "transform 0.15s ease, opacity 0.15s ease",
              display: "inline-flex",
              alignItems: "center"
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-1px)";
              e.currentTarget.style.opacity = "0.9";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.opacity = "1";
            }}
          >
            Launch console <Icon name="arrow" size={17} />
          </Link>
        </div>
      </section>
    </>
  );
}