import { api } from "../../../services/api/client";

export interface State {
  id: number;
  state_name: string;
  state_code: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface District {
  id: number;
  division_id: number;
  district_name: string;
  district_code: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export async function getStates() {
  const response = await api.get<State[]>("/states/");
  return response.data;
}

export async function getDistricts() {
  const response = await api.get<District[]>("/districts/");
  return response.data;
}
