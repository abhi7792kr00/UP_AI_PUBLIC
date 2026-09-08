import { Link } from "react-router-dom";
import { FilePlus2, Filter, Search } from "lucide-react";
import { complaints } from "../data/mock";
import { Badge, Button, Card, Input, PageHeader, StatCard } from "../components/ui";

export function Complaints() {
  return <div className="page">
    <PageHeader eyebrow="CITIZEN WORKSPACE" title="My complaints" description="Monitor every submitted complaint and its current workflow state." action={<Link className="btn btn-primary" to="/complaints/new"><FilePlus2 size={17}/> New complaint</Link>} />
    <div className="stats-grid four"><StatCard label="Total complaints" value="24" trend="+3 this month" /><StatCard label="Active" value="8" trend="2 due today" /><StatCard label="Resolved" value="16" trend="89% satisfaction" /><StatCard label="SLA compliance" value="93%" trend="+4.2% this quarter" /></div>
    <Card className="table-wrap">
      <div className="toolbar"><div className="toolbar-search"><Search size={17}/><Input placeholder="Search complaint number or category..." /></div><Button variant="secondary"><Filter size={16}/> Filters</Button></div>
      <div className="data-table"><div className="table-head"><span>Complaint</span><span>Department</span><span>Status</span><span>SLA</span><span></span></div>
      {complaints.map(c => <Link className="table-row" to={`/complaints/${c.id}`} key={c.id}><div><strong>{c.id}</strong><small>{c.category} · {c.location}</small></div><span>{c.department}</span><Badge tone={c.status === "RESOLVED" ? "success" : c.status === "ESCALATED" ? "danger" : "info"}>{c.status.replace("_"," ")}</Badge><span>{c.slaHours ? `${c.slaHours}h` : "—"}</span><span>→</span></Link>)}</div>
    </Card>
  </div>;
}