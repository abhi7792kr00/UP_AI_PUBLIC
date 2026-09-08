import { useQueryClient } from "@tanstack/react-query";
import { useAuthStore } from "../../../stores/auth.store";

export function useLogout() {
  const clearAuth = useAuthStore((s) => s.clearAuth);
  const queryClient = useQueryClient();

  return () => {
    clearAuth();
    queryClient.clear();
    try {
      sessionStorage.clear();
    } catch {
      // ignore
    }
  };
}
