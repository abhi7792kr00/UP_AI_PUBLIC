import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../../../stores/auth.store";

interface RoleGuardProps {
  allowedRoles: number[];
  redirectTo?: string;
}

export function RoleGuard({
  allowedRoles,
  redirectTo = "/login/citizen",
}: RoleGuardProps) {
  const user = useAuthStore((state) => state.user);

  if (!user) {
    return <Navigate to={redirectTo} replace />;
  }

  if (!allowedRoles.includes(user.role_id)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <Outlet />;
}
