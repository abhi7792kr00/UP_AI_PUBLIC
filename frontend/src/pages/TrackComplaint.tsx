import { useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, CheckCircle2, Clock3, Search, ShieldCheck } from "lucide-react";
import { complaints } from "../data/mock";
import { Button, Card, Input, PageHeader, Badge } from "../components/ui";
import { toast } from "sonner";

export function TrackComplaint() {
  const [id, setId] = useState("");
  const [result, setResult] = useState(complaints[0]);

  const search = () => {
    const found = complaints.find(c => c.id.toLowerCase() === id.trim().toLowerCase()) ?? complaints[0];
    setResult(found);
    toast.success("Complaint record loaded");
  };

  return <div className="container page">
    <PageHeader eyebrow="PUBLIC TRACKING" title="Track your complaint" description="Enter your complaint number to see its current office, officer, status and SLA." />
    <Card className="track-search"><Search size={20}/><Input value={id} onChange={e => setId(e.target.value)} placeholder="Example: UP-2026-00018452" onKeyDown={e => e.key === "Enter" && search()}/><Button onClick={search}>Track</Button></Card>
    <div className="tracking-grid">
      <Card>
        <div className="record-header"><div><span className="eyebrow">COMPLAINT NUMBER</span><h2>{result.id}</h2></div><Badge tone={result.status === "ESCALATED" ? "danger" : result.status === "RESOLVED" ? "success" : "info"}>{result.status.replace("_"," ")}</Badge></div>
        <h3>{result.category}</h3><p>{result.summary}</p>
        <div className="detail-grid">
          <div><span>Department</span><strong>{result.department}</strong></div><div><span>Current office</span><strong>{result.currentOffice}</strong></div>
          <div><span>Current officer</span><strong>{result.currentOfficer}</strong></div><div><span>Location</span><strong>{result.location}</strong></div>
        </div>
        <Link className="inline-link" to={`/complaints/${result.id}`}>Open full timeline <ArrowRight size={16}/></Link>
      </Card>
      <Card>
        <div className="sla-card"><Clock3 size={22}/><div><span>SLA remaining</span><strong>{result.slaHours ? `${result.slaHours} hours` : "Completed"}</strong></div></div>
        <div className="progress"><div style={{width:`${result.progress}%`}}/></div>
        <div className="progress-label"><span>Workflow progress</span><strong>{result.progress}%</strong></div>
        <div className="track-points"><div><CheckCircle2/> Complaint received</div><div><CheckCircle2/> Department routed</div><div><CheckCircle2/> Officer assigned</div><div className="current"><ShieldCheck/> Current action in progress</div></div>
      </Card>
    </div>
  </div>;
}