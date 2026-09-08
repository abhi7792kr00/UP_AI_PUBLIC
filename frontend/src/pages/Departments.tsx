import { Link } from "react-router-dom";
import { ArrowRight, Building2, FileText, Search } from "lucide-react";
import { departmentStats } from "../data/mock";
import { Card, Input, PageHeader, StatCard } from "../components/ui";

export function Departments() {
  return <div className="container page">
    <PageHeader eyebrow="PUBLIC DIRECTORY" title="Government departments" description="Browse department services, complaint volumes and performance indicators." />
    <Card className="directory-toolbar"><div className="toolbar-search"><Search size={17}/><Input placeholder="Search department..." /></div></Card>
    <div className="stats-grid three"><StatCard label="Departments tracked" value="42" /><StatCard label="Districts connected" value="75" /><StatCard label="Complaints this year" value="12.4L" trend="Demo analytics" /></div>
    <div className="department-list">{departmentStats.map(d => <Link to="/analytics" className="department-row" key={d.name}><div className="department-icon"><Building2 size={20}/></div><div className="department-name"><strong>{d.name}</strong><span><FileText size={14}/> {d.complaints.toLocaleString()} complaints</span></div><div className="department-metrics"><span>Pending <strong>{d.pending.toLocaleString()}</strong></span><span>Resolved <strong>{d.resolved.toLocaleString()}</strong></span></div><ArrowRight size={18}/></Link>)}</div>
  </div>;
}