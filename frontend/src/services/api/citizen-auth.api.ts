import { api } from "./client";

export interface CitizenRegistrationPayload {
  full_name: string;
  username: string;
  email: string;
  mobile: string;
  password: string;

  father_name?: string | null;
  mother_name?: string | null;
  gender?: string | null;
  dob?: string | null;

  address: string;
  pincode?: string | null;

  state_id: number;
  district_id: number;

  area_type: "rural" | "urban";

  tehsil_id?: number | null;
  block_id?: number | null;
  gram_panchayat_id?: number | null;
  village_id?: number | null;

  municipal_body_id?: number | null;
  ward_id?: number | null;
  locality_id?: number | null;
}

export interface CitizenOtpRequestResponse {
  registration_id: number;
  message: string;
}

export interface CitizenOtpVerifyResponse {
  user_id: number;
  citizen_id: number;
  message: string;
}

export async function requestCitizenRegistrationOtp(
  payload: CitizenRegistrationPayload,
) {
  const response =
    await api.post<CitizenOtpRequestResponse>(
      "/auth/citizen/register/request-otp",
      payload,
    );

  return response.data;
}

export async function verifyCitizenRegistrationOtp(
  registration_id: number,
  otp: string,
) {
  const response =
    await api.post<CitizenOtpVerifyResponse>(
      "/auth/citizen/register/verify-otp",
      {
        registration_id,
        otp,
      },
    );

  return response.data;
}