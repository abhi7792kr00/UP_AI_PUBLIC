import { useMutation } from "@tanstack/react-query";

import {
  requestPasswordReset,
  verifyPasswordResetOtp,
  resetPassword,
  requestUsernameRecovery,
  verifyUsernameRecoveryOtp,
} from "../../../services/api/recovery.api";

export function useRequestPasswordReset() {
  return useMutation({
    mutationFn: (identifier: string) =>
      requestPasswordReset(identifier),
  });
}

export function useVerifyPasswordResetOtp() {
  return useMutation({
    mutationFn: ({
      recoveryId,
      otp,
    }: {
      recoveryId: number;
      otp: string;
    }) =>
      verifyPasswordResetOtp(recoveryId, otp),
  });
}

export function useResetPassword() {
  return useMutation({
    mutationFn: ({
      recoveryId,
      newPassword,
    }: {
      recoveryId: number;
      newPassword: string;
    }) =>
      resetPassword(recoveryId, newPassword),
  });
}

export function useRequestUsernameRecovery() {
  return useMutation({
    mutationFn: (identifier: string) =>
      requestUsernameRecovery(identifier),
  });
}

export function useVerifyUsernameRecoveryOtp() {
  return useMutation({
    mutationFn: ({
      recoveryId,
      otp,
    }: {
      recoveryId: number;
      otp: string;
    }) =>
      verifyUsernameRecoveryOtp(recoveryId, otp),
  });
}
