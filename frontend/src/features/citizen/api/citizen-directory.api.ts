import { api } from "../../../services/api/client";

export interface District {
  id: number;
  district_name: string;
  state_id?: number;
}

export interface Tehsil {
  id: number;
  tehsil_name: string;
  district_id?: number;
}

export interface Block {
  id: number;
  block_name: string;
  district_id?: number;
  tehsil_id?: number;
}

export interface CitizenDepartment {
  id: number;
  department_name: string;
  department_code: string;
  description: string | null;
  is_active: boolean;
}

export interface Officer {
  id: number;
  full_name?: string;
  name?: string;
  designation?: string;
  department_id?: number;
  district_id?: number;
  mobile?: string | null;
  email?: string | null;
  is_active?: boolean;
}

export async function getDistricts() {
  const response = await api.get<District[]>("/districts/");
  return response.data;
}

export async function getTehsils() {
  const response = await api.get<Tehsil[]>("/tehsils/");
  return response.data;
}

export async function getBlocks() {
  const response = await api.get<Block[]>("/blocks/");
  return response.data;
}

export async function getCitizenDepartments() {
  const response = await api.get<CitizenDepartment[]>(
    "/departments/",
  );

  return response.data;
}

export async function getOfficers() {
  const response = await api.get<Officer[]>("/officers/");
  return response.data;
}
