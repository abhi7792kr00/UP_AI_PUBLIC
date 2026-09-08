import { Link } from "react-router-dom";
import { Activity, AlertTriangle, ArrowRight, CheckCircle2, Clock3, FileText, TrendingUp } from "lucide-react";
import ReactECharts from "echarts-for-react";
import { complaints, departmentStats } from "../data/mock";
import { Card, PageHeader, StatCard, Badge } from "../components/ui";

const chart = {
  tooltip: { trigger: "axis" },
  grid: { left: 0, right: 0, top: 20, bottom: 0, containLabel: true },
  xAxis: { type: "category", data: ["Mar","Apr","May","Jun","Jul","Aug"], boundaryGap: false },
  yAxis: { type: "value", splitLine: { lineStyle: { color: "#e5e7eb" } } },
  series: [{ data: [720, 880, 1020, 960, 1180, 1320], type: "line", smooth: true, areaStyle: { opacity: 0.08 }, lineStyle: { width: 3 } }],
};

export function Dashboard() {
  return <div className="page">
    <PageHeader eyebrow="CITIZEN COMMAND CENTER" title="Good morning, Citizen." description="Here is the current status of your service requests and complaints." action={<Link className="btn btn-primary" to="/complaints/new"><FileText size={17}/> File complaint</Link>} />
    <div className="stats-grid four">
      <StatCard label="Total complaints" value="24" trend="+3 this month" icon={<FileText/>}/>
      <StatCard label="Active cases" value="8" trend="2 due today" icon={<Activity/>}/>
      <StatCard label="Resolved" value="16" trend="89% satisfaction" icon={<CheckCircle2/>}/>
      <StatCard label="SLA at risk" value="2" trend="Requires attention" icon={<AlertTriangle/>}/>
    </div>
    <div className="dashboard-grid">
      <Card className="chart-card"><div className="card-heading"><div><h3>Complaint activity</h3><p>Last six months</p></div><Badge tone="success"><TrendingUp size={14}/> +18.4%</Badge></div><ReactECharts option={chart} style={{height:280}} /></Card>
      <Card><div className="card-heading"><div><h3>Current cases</h3><p>Your latest activity</p></div><Link className="text-link" to="/complaints">View all</Link></div><div className="compact-list">{complaints.map(c => <Link className="compact-row" to={`/complaints/${c.id}`} key={c.id}><div><strong>{c.category}</strong><span>{c.id}</span></div><Badge tone={c.status === "RESOLVED" ? "success" : c.status === "ESCALATED" ? "danger" : "info"}>{c.status.replace("_"," ")}</Badge></Link>)}</div></Card>
    </div>
    <div className="dashboard-grid bottom"><Card><div className="card-heading"><div><h3>Department performance</h3><p>Current demo data</p></div></div><div className="mini-bars">{departmentStats.slice(0,5).map(d => <div className="mini-bar" key={d.name}><div><span>{d.name}</span><strong>{Math.round(d.resolved/d.complaints*100)}%</strong></div><div className="progress"><div style={{width:`${Math.round(d.resolved/d.complaints*100)}%`}}/></div></div>)}</div></Card><Card><div className="card-heading"><div><h3>Next actions</h3><p>Keep your complaints moving.</p></div></div><div className="action-list"><div><Clock3/><span><strong>2 complaints</strong> have SLA deadlines today.</span><ArrowRight/></div><div><AlertTriangle/><span><strong>1 response</strong> is waiting for citizen input.</span><ArrowRight/></div></div></Card></div>
  </div>;
}