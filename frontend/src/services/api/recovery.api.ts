import { api } from "./client";

export interface RecoveryResponse {
  recovery_id: number;
  message: string;
}

export interface UsernameRecoveryResponse {
  recovery_id: number;
  username: string;
  message: string;
}

export async function requestPasswordReset(
  identifier: string,
): Promise<RecoveryResponse> {
  const response = await api.post<RecoveryResponse>(
    "/auth/forgot-password",
    {
      identifier,
    },
  );

  return response.data;
}

export async function verifyPasswordResetOtp(
  recoveryId: number,
  otp: string,
): Promise<RecoveryResponse> {
  const response = await api.post<RecoveryResponse>(
    "/auth/forgot-password/verify-otp",
    {
      recovery_id: recoveryId,
      otp,
    },
  );

  return response.data;
}

export async function resetPassword(
  recoveryId: number,
  newPassword: string,
): Promise<RecoveryResponse> {
  const response = await api.post<RecoveryResponse>(
    "/auth/forgot-password/reset",
    {
      recovery_id: recoveryId,
      new_password: newPassword,
    },
  );

  return response.data;
}

export async function requestUsernameRecovery(
  identifier: string,
): Promise<RecoveryResponse> {
  const response = await api.post<RecoveryResponse>(
    "/auth/forgot-username",
    {
      identifier,
    },
  );

  return response.data;
}

export async function verifyUsernameRecoveryOtp(
  recoveryId: number,
  otp: string,
): Promise<UsernameRecoveryResponse> {
  const response = await api.post<UsernameRecoveryResponse>(
    "/auth/forgot-username/verify-otp",
    {
      recovery_id: recoveryId,
      otp,
    },
  );

  return response.data;
}
