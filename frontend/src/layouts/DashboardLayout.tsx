import { Outlet, Link, useLocation } from "react-router-dom";
import { BarChart3, Bot, ChevronLeft, FileText, Home, LayoutDashboard, Menu, Settings, ShieldCheck, Users, Building2 } from "lucide-react";
import { useUIStore } from "../stores/ui";
import { TopSearch } from "./PublicLayout";

const items = [
  ["/dashboard", "Overview", LayoutDashboard],
  ["/complaints", "Complaints", FileText],
  ["/officers", "Officers", Users],
  ["/departments", "Departments", Building2],
  ["/analytics", "Analytics", BarChart3],
  ["/ai", "AI Assistant", Bot],
];

export function DashboardLayout() {
  const { sidebarOpen, toggleSidebar } = useUIStore();
  const location = useLocation();

  return (
    <div className="dashboard-shell">
      <aside className={sidebarOpen ? "sidebar" : "sidebar collapsed"}>
        <Link to="/" className="sidebar-brand"><ShieldCheck size={21} /><span>UP_AI</span></Link>
        <div className="side-label">WORKSPACE</div>
        <nav>
          {items.map(([href, label, Icon]) => {
            const C = Icon as typeof Home;
            const active = location.pathname === href || (href === "/complaints" && location.pathname.startsWith("/complaints/"));
            return <Link className={active ? "side-link active" : "side-link"} to={href as string} key={href as string}><C size={18} /><span>{label as string}</span></Link>;
          })}
        </nav>
        <div className="sidebar-bottom">
          <Link className="side-link" to="/"><Home size={18}/><span>Public Portal</span></Link>
          <button className="side-link" onClick={toggleSidebar}><ChevronLeft size={18}/><span>{sidebarOpen ? "Collapse" : "Expand"}</span></button>
        </div>
      </aside>
      <section className="dashboard-main">
        <header className="dashboard-topbar">
          <button className="icon-button mobile-menu" onClick={toggleSidebar}><Menu /></button>
          <TopSearch />
          <div className="topbar-user"><div className="avatar">C</div><div><strong>Citizen</strong><span>Citizen Portal</span></div></div>
        </header>
        <div className="dashboard-content"><Outlet /></div>
      </section>
    </div>
  );
}