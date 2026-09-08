import { create } from "zustand";

import type { CurrentUser } from "../services/api/auth.api";

interface AuthState {
  user: CurrentUser | null;
  isAuthenticated: boolean;

  setUser: (user: CurrentUser) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: Boolean(
    localStorage.getItem("upai_access_token"),
  ),

  setUser: (user) =>
    set({
      user,
      isAuthenticated: true,
    }),

  clearAuth: () => {
    localStorage.removeItem("upai_access_token");

    set({
      user: null,
      isAuthenticated: false,
    });
  },
}));
