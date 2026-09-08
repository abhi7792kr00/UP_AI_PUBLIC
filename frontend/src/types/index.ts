export type Role = "CITIZEN" | "OFFICER" | "DISTRICT_ADMIN" | "STATE_ADMIN" | "SUPER_ADMIN";

export type ComplaintStatus = "SUBMITTED" | "IN_REVIEW" | "ASSIGNED" | "INVESTIGATION" | "RESOLVED" | "ESCALATED";

export interface Complaint {
  id: string;
  category: string;
  department: string;
  location: string;
  status: ComplaintStatus;
  priority: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  currentOffice: string;
  currentOfficer: string;
  submittedAt: string;
  slaHours: number;
  progress: number;
  summary: string;
}

export interface Officer {
  id: string;
  name: string;
  designation: string;
  department: string;
  district: string;
  office: string;
  joined: string;
  rating: number;
  complaints: number;
  resolved: number;
  sla: number;
}

export interface TimelineEvent {
  title: string;
  office: string;
  officer: string;
  time: string;
  done: boolean;
  description: string;
}