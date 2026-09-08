import type { Complaint, Officer, TimelineEvent } from "../types";

export const complaints: Complaint[] = [
  {
    id: "UP-2026-00018452",
    category: "Water Supply",
    department: "Panchayati Raj",
    location: "Darvepur, Saidpur, Ghazipur",
    status: "INVESTIGATION",
    priority: "HIGH",
    currentOffice: "Block Development Office",
    currentOfficer: "Assigned Development Officer",
    submittedAt: "19 Aug 2026, 09:32",
    slaHours: 32,
    progress: 72,
    summary: "Public handpump has remained non-functional and residents are facing water-supply difficulty.",
  },
  {
    id: "UP-2026-00018421",
    category: "Road & Drainage",
    department: "Rural Development",
    location: "Saidpur",
    status: "ASSIGNED",
    priority: "MEDIUM",
    currentOffice: "Block Office",
    currentOfficer: "Field Officer",
    submittedAt: "18 Aug 2026, 16:10",
    slaHours: 54,
    progress: 48,
    summary: "Drainage blockage reported near the main village road.",
  },
  {
    id: "UP-2026-00018390",
    category: "Revenue",
    department: "Revenue Department",
    location: "Ghazipur",
    status: "RESOLVED",
    priority: "LOW",
    currentOffice: "Tehsil Office",
    currentOfficer: "Revenue Officer",
    submittedAt: "16 Aug 2026, 11:20",
    slaHours: 0,
    progress: 100,
    summary: "Request regarding correction of land record entry.",
  },
  {
    id: "UP-2026-00018280",
    category: "Electricity",
    department: "Energy Department",
    location: "Ghazipur",
    status: "ESCALATED",
    priority: "CRITICAL",
    currentOffice: "District Administration",
    currentOfficer: "District Nodal Officer",
    submittedAt: "14 Aug 2026, 10:05",
    slaHours: 0,
    progress: 83,
    summary: "Repeated electricity interruption reported by multiple residents.",
  },
];

export const officers: Officer[] = [
  { id: "off-001", name: "Aarav Singh", designation: "District Nodal Officer", department: "District Administration", district: "Ghazipur", office: "District Collectorate", joined: "12 Jun 2024", rating: 4.5, complaints: 624, resolved: 581, sla: 93 },
  { id: "off-002", name: "Priya Sharma", designation: "Development Officer", department: "Rural Development", district: "Ghazipur", office: "Block Development Office", joined: "04 Sep 2023", rating: 4.3, complaints: 428, resolved: 391, sla: 91 },
  { id: "off-003", name: "Vivek Kumar", designation: "Revenue Officer", department: "Revenue Department", district: "Ghazipur", office: "Tehsil Office", joined: "18 Jan 2025", rating: 4.1, complaints: 312, resolved: 286, sla: 89 },
  { id: "off-004", name: "Neha Verma", designation: "Health Program Officer", department: "Health Department", district: "Ghazipur", office: "District Health Office", joined: "21 Jul 2022", rating: 4.6, complaints: 510, resolved: 482, sla: 95 },
];

export const timeline: TimelineEvent[] = [
  { title: "Complaint Created", office: "UP_AI Citizen Portal", officer: "System", time: "19 Aug · 09:32", done: true, description: "Complaint submitted successfully and complaint number generated." },
  { title: "Department Received", office: "Panchayati Raj Department", officer: "Department Desk", time: "19 Aug · 10:04", done: true, description: "Complaint classified and routed to the responsible department." },
  { title: "Block Office", office: "Block Development Office", officer: "Office Desk", time: "19 Aug · 12:18", done: true, description: "Complaint forwarded to the local office for action." },
  { title: "Officer Assigned", office: "Block Development Office", officer: "Assigned Development Officer", time: "19 Aug · 13:05", done: true, description: "Complaint assigned to an officer for field verification." },
  { title: "Investigation", office: "Block Development Office", officer: "Assigned Development Officer", time: "Current", done: false, description: "Field verification and action are currently in progress." },
  { title: "Resolution", office: "—", officer: "—", time: "Pending", done: false, description: "Final resolution will appear here after action is completed." },
];

export const departmentStats = [
  { name: "Revenue", complaints: 2840, pending: 382, resolved: 2458 },
  { name: "Police", complaints: 2120, pending: 310, resolved: 1810 },
  { name: "Rural Development", complaints: 1340, pending: 178, resolved: 1162 },
  { name: "Health", complaints: 920, pending: 94, resolved: 826 },
  { name: "Education", complaints: 840, pending: 76, resolved: 764 },
  { name: "Municipal", complaints: 710, pending: 112, resolved: 598 },
];