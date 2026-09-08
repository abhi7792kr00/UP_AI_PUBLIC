import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuthStore } from "../../../stores/auth.store";

export function ProtectedRoute() {
  const location = useLocation();

  const isAuthenticated = useAuthStore(
    (state) => state.isAuthenticated,
  );

  if (!isAuthenticated) {
    return (
      <Navigate
        to="/login/citizen"
        replace
        state={{ from: location.pathname }}
      />
    );
  }

  return <Outlet />;
}
