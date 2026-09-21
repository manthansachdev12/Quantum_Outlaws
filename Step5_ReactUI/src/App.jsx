import React, { useEffect, useState } from "react";
import { NavLink, Route, Routes, useLocation } from "react-router-dom";
import Home from "./pages/Home";
import RiskIndicator from "./pages/RiskIndicator";
import Prototype from "./pages/Prototype";
import { api } from "./lib/api";

function Icon({ name, size = 18 }) {
  const common = { width: size, height: size, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.7, strokeLinecap: "round", strokeLinejoin: "round" };
  const paths = {
    home: <><path d="M3 10.5 12 3l9 7.5"/><path d="M5.5 9.5V21h13V9.5"/><path d="M9.5 21v-6h5v6"/></>,
    pulse: <><path d="M3 12h4l2-6 4 12 2-6h6"/></>,
    shield: <><path d="M12 3 20 6v6c0 5-3.2 8-8 9-4.8-1-8-4-8-9V6l8-3Z"/><path d="m9 12 2 2 4-4"/></>,
    activity: <><path d="M4 19V5"/><path d="M4 19h16"/><path d="m7 15 3-4 3 2 4-6"/></>,
    arrow: <><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></>,
    external: <><path d="M14 4h6v6"/><path d="M10 14 20 4"/><path d="M20 14v5H5V4h5"/></>,
    terminal: <><path d="m6 8 4 4-4 4"/><path d="M13 16h5"/></>,
    check: <path d="m5 12 4 4L19 6"/>,
    alert: <><path d="M12 3 22 20H2L12 3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></>,
    menu: <><path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/></>,
  };
  return <svg {...common}>{paths[name] || paths.activity}</svg>;
}

function Navbar({ online }) {
  const [open, setOpen] = useState(false);
  const location = useLocation();

  useEffect(() => setOpen(false), [location.pathname]);

  return (
    <header className="navbar">
      <div className="nav-inner">
        <NavLink to="/" className="brand">
          <span className="brand-mark"><span /></span>
          <span className="brand-copy">
            <strong>Q-SHIELD</strong>
            <small>QUANTUM SIGNATURE SECURITY</small>
          </span>
        </NavLink>

        <button className="mobile-menu" onClick={() => setOpen(v => !v)} aria-label="Open navigation">
          <Icon name="menu" />
        </button>

        <nav className={`nav-links ${open ? "open" : ""}`}>
          <NavLink to="/" end className="nav-link">
            <Icon name="home" size={16} /> Overview
          </NavLink>
          <NavLink to="/risk" className="nav-link">
            <Icon name="pulse" size={16} /> Risk Indicator
          </NavLink>
          <NavLink to="/prototype" className="nav-link nav-primary">
            <Icon name="shield" size={16} /> Prototype
          </NavLink>
        </nav>

        <div className="system-status">
          <span className={`status-dot ${online ? "online" : "offline"}`} />
          <span>{online ? "API ONLINE" : "API OFFLINE"}</span>
        </div>
      </div>
    </header>
  );
}

export default function App() {
  const [online, setOnline] = useState(false);

  useEffect(() => {
    let active = true;
    api.health()
      .then(() => active && setOnline(true))
      .catch(() => active && setOnline(false));

    const timer = setInterval(() => {
      api.health()
        .then(() => active && setOnline(true))
        .catch(() => active && setOnline(false));
    }, 8000);

    return () => {
      active = false;
      clearInterval(timer);
    };
  }, []);

  return (
    <div className="app-shell">
      <Navbar online={online} />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/risk" element={<RiskIndicator />} />
          <Route path="/prototype" element={<Prototype />} />
        </Routes>
      </main>
      <footer className="site-footer">
        <div>
          <span className="footer-brand">Q-SHIELD</span>
          <span className="footer-muted">SIH26141 · Quantum Outlaws</span>
        </div>
        <div className="footer-muted">Quantum-principle detection · No AI/ML</div>
      </footer>
    </div>
  );
}

export { Icon };
