import { api } from "../../../services/api/client";

export interface District {
  id: number;
  district_name: string;
  district_code: string;
}

export interface Tehsil {
  id: number;
  tehsil_name: string;
  tehsil_code: string;
  district_id: number;
}

export interface Block {
  id: number;
  block_name: string;
  block_code: string;
  tehsil_ids: number[];
}

export interface MunicipalBody {
  id: number;
  body_name: string;
  body_code: string;
  body_type:
    | "NAGAR_NIGAM"
    | "NAGAR_PALIKA_PARISHAD"
    | "NAGAR_PANCHAYAT"
    | "NOTIFIED_AREA_COUNCIL"
    | "CANTONMENT_BOARD";
  district_id: number;
  headquarters?: string | null;
  is_active?: boolean;
}

export interface Ward {
  id: number;
  ward_name: string;
  ward_number: number;
  municipal_body_id: number;
  population?: number | null;
  is_active?: boolean;
}

export interface Locality {
  id: number;
  locality_name: string;
  locality_code: string;
  ward_id: number;
  pincode?: string | null;
  is_active?: boolean;
}

export interface GovernmentDepartment {
  id: number;
  department_name: string;
  department_code: string;
  description?: string | null;
  is_active?: boolean;
}

export interface Designation {
  id: number;
  designation_name: string;
  designation_code: string;
  description?: string | null;
  department_id: number;
  is_active?: boolean;
}

export interface Office {
  id: number;
  office_name: string;
  office_code: string;
  address?: string | null;
  phone?: string | null;
  email?: string | null;
  department_id: number;
  district_id?: number | null;
  tehsil_id?: number | null;
  block_id?: number | null;
  municipal_body_id?: number | null;
  ward_id?: number | null;
  locality_id?: number | null;
  is_active?: boolean;
}

export interface Officer {
  id: number;
  officer_name: string;
  employee_code: string;
  mobile?: string | null;
  email?: string | null;
  department_id: number;
  designation_id: number;
  office_id: number;
  district_id?: number | null;
  tehsil_id?: number | null;
  block_id?: number | null;
  is_active: boolean;
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

export interface GramPanchayat {
  id: number;
  block_id: number;
  gram_panchayat_name: string;
  gram_panchayat_code: string;
  is_active?: boolean;
}

export interface Village {
  id: number;
  gram_panchayat_id: number | null;
  village_name: string;
  village_code: string;
  is_active?: boolean;
}

export async function getGramPanchayatsByBlock(
  blockId: number,
) {
  const response =
    await api.get<GramPanchayat[]>(
      `/gram-panchayats/block/${blockId}`,
    );

  return response.data;
}

export async function getVillagesByGramPanchayat(
  gramPanchayatId: number,
) {
  const response =
    await api.get<Village[]>(
      `/villages/gram-panchayat/${gramPanchayatId}`,
    );

  return response.data;
}

export async function getMunicipalBodies() {
  const response = await api.get<MunicipalBody[]>(
    "/municipal-bodies/",
  );

  return response.data;
}

export async function getWards() {
  const response = await api.get<Ward[]>(
    "/wards/",
  );

  return response.data;
}

export async function getLocalities() {
  const response = await api.get<Locality[]>(
    "/localities/",
  );

  return response.data;
}

export async function getGovernmentDepartments() {
  const response = await api.get<GovernmentDepartment[]>(
    "/departments/",
  );
  return response.data;
}

export async function getDesignations() {
  const response = await api.get<Designation[]>(
    "/designations/",
  );
  return response.data;
}

export async function getOffices() {
  const response = await api.get<Office[]>("/offices/");
  return response.data;
}

export async function getOfficers() {
  const response = await api.get<Officer[]>("/officers/");
  return response.data;
}
