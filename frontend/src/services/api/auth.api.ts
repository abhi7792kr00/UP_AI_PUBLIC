import { api } from "./client";

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface CurrentUserCitizen {
  id: number;

  father_name: string | null;
  mother_name: string | null;

  gender: string | null;
  dob: string | null;

  address: string;
  pincode: string | null;

  state_id: number;
  district_id: number;

  area_type: "rural" | "urban";

  tehsil_id: number | null;
  block_id: number | null;
  gram_panchayat_id: number | null;
  village_id: number | null;

  municipal_body_id: number | null;
  ward_id: number | null;
  locality_id: number | null;
}

export interface CurrentUser {
  id: number;
  full_name: string;
  username: string;
  email: string | null;
  mobile: string | null;
  is_active: boolean;
  role_id: number;

  citizen: CurrentUserCitizen | null;
}

export async function loginUser(
  username: string,
  password: string,
): Promise<LoginResponse> {
  const formData = new URLSearchParams();

  formData.append("username", username);
  formData.append("password", password);

  const response = await api.post<LoginResponse>(
    "/auth/login",
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    },
  );

  return response.data;
}

export async function getCurrentUser(): Promise<CurrentUser> {
  const response = await api.get<CurrentUser>("/auth/me");

  return response.data;
}
