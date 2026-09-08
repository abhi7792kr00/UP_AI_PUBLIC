import { api } from "../../../services/api/client";

export interface ComplaintCategory {
  id: number;
  category_name: string;
  category_code: string;
  description: string | null;
  icon: string | null;
  color: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Department {
  id: number;
  department_name: string;
  department_code: string;
  description: string | null;
  is_active: boolean;
}

export interface ComplaintStatus {
  id: number;
  status_name: string;
  status_code: string;
  display_order: number;
  is_final: boolean;
  allow_reopen: boolean;
  color: string | null;
  description: string | null;
}

export async function getComplaintCategories() {
  const response = await api.get<ComplaintCategory[]>(
    "/complaint-categories/",
  );

  return response.data;
}

export async function getDepartments() {
  const response = await api.get<Department[]>(
    "/departments/",
  );

  return response.data;
}

export async function getComplaintStatuses() {
  const response = await api.get<ComplaintStatus[]>(
    "/complaint-statuses/",
  );

  return response.data;
}
