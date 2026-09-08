import { useQuery } from "@tanstack/react-query";

import { getCurrentUser } from "../../../services/api/auth.api";
import { useAuthStore } from "../../../stores/auth.store";

export function useCurrentUser() {
  const token = localStorage.getItem("upai_access_token");
  const setUser = useAuthStore((state) => state.setUser);

  return useQuery({
    queryKey: ["current-user"],
    queryFn: async () => {
      const user = await getCurrentUser();
      setUser(user);
      return user;
    },
    enabled: Boolean(token),
    retry: false,
  });
}
