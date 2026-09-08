import { useMutation } from "@tanstack/react-query";

import {
  requestCitizenRegistrationOtp,
  verifyCitizenRegistrationOtp,
  type CitizenRegistrationPayload,
} from "../../../services/api/citizen-auth.api";

export function useCitizenOtpRegistration() {
  const requestOtpMutation = useMutation({
    mutationFn: (
      payload: CitizenRegistrationPayload,
    ) => requestCitizenRegistrationOtp(payload),
  });

  const verifyOtpMutation = useMutation({
    mutationFn: ({
      registration_id,
      otp,
    }: {
      registration_id: number;
      otp: string;
    }) =>
      verifyCitizenRegistrationOtp(
        registration_id,
        otp,
      ),
  });

  return {
    requestOtpMutation,
    verifyOtpMutation,
  };
}
