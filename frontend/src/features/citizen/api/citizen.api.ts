import { api } from "../../../services/api/client";

export interface CitizenComplaintOfficer {
  id: number;
  officer_name: string;
  photo_url: string | null;
  mobile: string | null;
  email: string | null;
  designation_name: string | null;
  department_name: string | null;
  office_name: string | null;
}

export interface CitizenComplaint {
  id: number;
  complaint_number: string;
  subject: string;
  description: string;
  category_id: number;
  subcategory_id: number | null;
  priority_id: number | null;
  status_id: number;
  department_id: number | null;
  office_id: number | null;
  assigned_officer_id: number | null;
  assigned_officer: CitizenComplaintOfficer | null;

  state_id: number;
  division_id: number | null;
  district_id: number;
  tehsil_id: number | null;
  block_id: number | null;
  gram_panchayat_id: number | null;
  village_id: number | null;
  municipal_body_id: number | null;
  ward_id: number | null;
  locality_id: number | null;
  address: string | null;
  latitude: number | null;
  longitude: number | null;
  pincode: string | null;
  mobile_number: string | null;
  email: string | null;
  has_attachment: boolean;
  source: string;
  language: string | null;
  visibility: string;
  created_at: string;
  updated_at: string;
}

export interface CitizenComplaintCreate {
  category_id: number;
  subcategory_id?: number | null;
  subject: string;
  description: string;
  priority_id?: number | null;
  state_id: number;
  division_id?: number | null;
  district_id: number;
  tehsil_id?: number | null;
  block_id?: number | null;
  gram_panchayat_id?: number | null;
  village_id?: number | null;
  municipal_body_id?: number | null;
  ward_id?: number | null;
  locality_id?: number | null;
  address?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  pincode?: string | null;
  mobile_number?: string | null;
  email?: string | null;
  has_attachment?: boolean;
  source?: string;
  language?: string | null;
  visibility?: string;
}

export interface ComplaintFeedbackCreate {
  rating: number;
  feedback_text?: string | null;
  is_satisfied?: boolean;
}

export interface ComplaintFeedbackResponse {
  id: number;
  complaint_id: number;
  citizen_id: number;
  rating: number;
  feedback_text: string | null;
  is_satisfied: boolean;
  created_at: string;
  updated_at: string;
}

export interface ComplaintTimeline {
  id: number;
  workflow_definition_id: number;
  workflow_step_id: number;
  reference_number: string;
  action: string;
  remarks: string | null;
  performed_by: number | null;
  created_at: string;
  updated_at: string;
}

export async function getMyComplaints() {
  const response = await api.get<CitizenComplaint[]>(
    "/citizen/complaints/",
  );

  return response.data;
}

export async function getMyComplaint(
  complaintNumber: string,
) {
  const response = await api.get<CitizenComplaint>(
    `/citizen/complaints/${encodeURIComponent(complaintNumber)}`,
  );

  return response.data;
}

export async function createMyComplaint(
  payload: CitizenComplaintCreate,
) {
  const response = await api.post<CitizenComplaint>(
    "/citizen/complaints/",
    payload,
  );

  return response.data;
}

export async function getComplaintTimeline(
  complaintNumber: string,
) {
  const response = await api.get<ComplaintTimeline[]>(
    `/complaints/${encodeURIComponent(complaintNumber)}/timeline`,
  );

  return response.data;
}

export async function getComplaintFeedback(
  complaintNumber: string,
) {
  const response = await api.get<ComplaintFeedbackResponse>(
    `/citizen/complaints/${encodeURIComponent(complaintNumber)}/feedback`,
  );

  return response.data;
}

export async function createComplaintFeedback(
  complaintNumber: string,
  payload: ComplaintFeedbackCreate,
) {
  const response = await api.post<ComplaintFeedbackResponse>(
    `/citizen/complaints/${encodeURIComponent(complaintNumber)}/feedback`,
    payload,
  );

  return response.data;
}
