import { Link } from "react-router-dom";
import { Search, MapPin, Star, ArrowRight } from "lucide-react";
import { officers } from "../data/mock";
import { Card, Input, PageHeader, Badge } from "../components/ui";

export function Officers() {
  return <div className="container page">
    <PageHeader eyebrow="PUBLIC DIRECTORY" title="Officer directory" description="Explore public service information and performance signals for government officers." />
    <Card className="directory-toolbar"><div className="toolbar-search"><Search size={17}/><Input placeholder="Search officer, designation or department..." /></div><select className="input compact"><option>All districts</option><option>Ghazipur</option><option>Varanasi</option></select></Card>
    <div className="officer-grid">{officers.map(o => <Link to={`/officers/${o.id}`} className="officer-card" key={o.id}><div className="officer-avatar">{o.name.split(" ").map(x=>x[0]).join("")}</div><div className="officer-head"><div><h3>{o.name}</h3><p>{o.designation}</p></div><Badge tone="success">{o.sla}% SLA</Badge></div><div className="officer-meta"><span><MapPin size={15}/>{o.district}</span><span><Star size={15}/>{o.rating} citizen rating</span></div><div className="officer-stats"><div><strong>{o.complaints}</strong><small>received</small></div><div><strong>{o.resolved}</strong><small>resolved</small></div><div><strong>{Math.round(o.resolved/o.complaints*100)}%</strong><small>resolution</small></div></div><span className="card-link">View profile <ArrowRight size={15}/></span></Link>)}</div>
  </div>;
}