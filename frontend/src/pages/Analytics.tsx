import ReactECharts from "echarts-for-react";
import { Download, Map, SlidersHorizontal } from "lucide-react";
import { Card, PageHeader, StatCard, Button } from "../components/ui";
import { departmentStats } from "../data/mock";

const option = {
  tooltip: { trigger: "axis" },
  legend: { data: ["Received","Resolved","Pending"] },
  grid: { left: 10, right: 20, top: 50, bottom: 10, containLabel: true },
  xAxis: { type: "category", data: departmentStats.map(x => x.name) },
  yAxis: { type: "value" },
  series: [
    { name: "Received", type: "bar", data: departmentStats.map(x => x.complaints) },
    { name: "Resolved", type: "bar", data: departmentStats.map(x => x.resolved) },
    { name: "Pending", type: "bar", data: departmentStats.map(x => x.pending) },
  ],
};

export function Analytics() {
  return <div className="page">
    <PageHeader eyebrow="GOVERNANCE ANALYTICS" title="Performance overview" description="Designed for district, department and state command-center APIs." action={<><Button variant="secondary"><SlidersHorizontal size={16}/> Filters</Button><Button variant="secondary"><Download size={16}/> Export</Button></>} />
    <div className="stats-grid four"><StatCard label="Total complaints" value="12,482" trend="+11.8%" /><StatCard label="Pending" value="1,842" trend="-4.2%" /><StatCard label="SLA compliance" value="92.7%" trend="+3.1%" /><StatCard label="Citizen satisfaction" value="4.3/5" trend="+0.2" /></div>
    <div className="dashboard-grid"><Card className="chart-card wide"><div className="card-heading"><div><h3>Department comparison</h3><p>Received vs resolved vs pending</p></div></div><ReactECharts option={option} style={{height:360}} /></Card><Card><div className="card-heading"><div><h3>District map</h3><p>GIS layer placeholder</p></div></div><div className="map-placeholder"><Map size={40}/><strong>UP district heatmap</strong><span>Leaflet/Mapbox can be connected without changing the page architecture.</span></div></Card></div>
  </div>;
}