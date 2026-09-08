import { useMutation } from "@tanstack/react-query";

import {
  getCurrentUser,
  loginUser,
} from "../../../services/api/auth.api";

import { useAuthStore } from "../../../stores/auth.store";

export function useLogin() {
  const setUser = useAuthStore((state) => state.setUser);

  return useMutation({
    mutationFn: async ({
      username,
      password,
    }: {
      username: string;
      password: string;
    }) => {
      const loginResponse = await loginUser(
        username,
        password,
      );

      localStorage.setItem(
        "upai_access_token",
        loginResponse.access_token,
      );

      const user = await getCurrentUser();

      return user;
    },

    onSuccess: (user) => {
      setUser(user);
    },
  });
}
