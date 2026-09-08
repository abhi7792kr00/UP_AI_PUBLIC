import { Outlet, Link, useLocation } from "react-router-dom";
import { Bell, Bot, ChevronDown, Menu, Search, ShieldCheck, UserRound } from "lucide-react";
import { useState } from "react";

export function PublicLayout() {
  const [open, setOpen] = useState(false);
  const location = useLocation();
  const nav = [
    ["/", "Home"],
    ["/track", "Track Complaint"],
    ["/officers", "Officers"],
    ["/departments", "Departments"],
  ];

  return (
    <div className="app">
      <header className="public-header">
        <Link className="brand" to="/">
          <div className="brand-mark"><ShieldCheck size={22} /></div>
          <div><strong>UP_AI</strong><span>Citizen Governance Platform</span></div>
        </Link>
        <nav className={open ? "desktop-nav open" : "desktop-nav"}>
          {nav.map(([href, label]) => <Link key={href} className={location.pathname === href ? "active" : ""} to={href}>{label}</Link>)}
          <Link className="ai-nav" to="/ai"><Bot size={16} /> Ask UP_AI</Link>
        </nav>
        <div className="header-actions">
          <button className="icon-button" aria-label="Notifications"><Bell size={18} /></button>
          <Link className="login-link" to="/login/citizen"><UserRound size={17} /> Login</Link>
          <button className="mobile-menu icon-button" onClick={() => setOpen(!open)} aria-label="Menu"><Menu /></button>
        </div>
      </header>
      <main><Outlet /></main>
      <footer className="footer">
        <div><strong>UP_AI</strong><p>Transparent, accountable and citizen-first governance.</p></div>
        <div><span>Citizen Services</span><span>Departments</span><span>Officer Directory</span><span>AI Assistant</span></div>
        <small>Frontend ready for FastAPI/OpenAPI integration · © 2026 UP_AI</small>
      </footer>
    </div>
  );
}

export function TopSearch() {
  return <div className="top-search"><Search size={17} /><input placeholder="Search complaints, officers, departments..." /><kbd>⌘ K</kbd></div>;
}