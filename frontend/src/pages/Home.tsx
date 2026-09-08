import { Link } from "react-router-dom";
import { ArrowRight, Bot, CheckCircle2, Clock3, FilePlus2, MapPin, Search, ShieldCheck, Sparkles, Users, Zap } from "lucide-react";
import { complaints } from "../data/mock";

export function Home() {
  return (
    <>
      <section className="hero">
        <div className="hero-copy">
          <div className="hero-pill"><Sparkles size={15}/> One platform for citizen governance</div>
          <h1>Government services,<br /><span>visible to citizens.</span></h1>
          <p>File a complaint, track every movement, discover responsible officers and get answers from UP_AI — from village and ward to district and state.</p>
          <div className="hero-actions">
            <Link className="btn btn-primary btn-lg" to="/complaints/new"><FilePlus2 size={18}/> File a Complaint</Link>
            <Link className="btn btn-secondary btn-lg" to="/track"><Search size={18}/> Track Complaint</Link>
          </div>
          <div className="trust-row"><span><CheckCircle2 size={16}/> Live complaint tracking</span><span><ShieldCheck size={16}/> Role-aware access</span><span><Bot size={16}/> AI-ready</span></div>
        </div>
        <div className="hero-panel">
          <div className="panel-top"><span>Complaint Command Center</span><span className="live-dot">● LIVE</span></div>
          <div className="hero-complaint">
            <div className="complaint-id">UP-2026-00018452 <span>HIGH</span></div>
            <h3>Public handpump not working</h3>
            <p>Darvepur, Saidpur, Ghazipur</p>
            <div className="mini-progress"><div style={{width:"72%"}}/></div>
            <div className="progress-label"><span>72% workflow progress</span><strong>32h SLA</strong></div>
            <div className="mini-timeline">
              <div className="done">Submitted <small>09:32</small></div>
              <div className="done">Department <small>10:04</small></div>
              <div className="done">Officer assigned <small>13:05</small></div>
              <div className="current">Investigation <small>Current</small></div>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-heading"><div><div className="eyebrow">CITIZEN FIRST</div><h2>Everything in one place.</h2></div><Link to="/dashboard">Open dashboard <ArrowRight size={16}/></Link></div>
        <div className="feature-grid">
          {[
            [FilePlus2, "File complaints", "Submit to the right department with guided, validated forms."],
            [Clock3, "Live tracking", "See the current office, officer, action and SLA at every step."],
            [Users, "Find officers", "Explore public service information, postings and citizen feedback."],
            [Bot, "Ask UP_AI", "Ask questions by text today, with voice and RAG-ready architecture."],
            [MapPin, "District intelligence", "Explore department performance and complaint hotspots."],
            [Zap, "Smart escalation", "SLA-aware workflows designed for faster resolution."],
          ].map(([Icon, title, desc]) => {
            const C = Icon as typeof Bot;
            return <div className="feature-card" key={title as string}><div className="feature-icon"><C size={20}/></div><h3>{title as string}</h3><p>{desc as string}</p></div>;
          })}
        </div>
      </section>

      <section className="section light-section">
        <div className="section-heading"><div><div className="eyebrow">RECENT ACTIVITY</div><h2>Transparent by design.</h2></div><Link to="/track">View tracking <ArrowRight size={16}/></Link></div>
        <div className="table-card">
          {complaints.slice(0,3).map(c => <Link className="activity-row" to={`/complaints/${c.id}`} key={c.id}><div><strong>{c.id}</strong><span>{c.category} · {c.location}</span></div><div><span className={`status status-${c.status.toLowerCase()}`}>{c.status.replace("_"," ")}</span><ArrowRight size={17}/></div></Link>)}
        </div>
      </section>
    </>
  );
}