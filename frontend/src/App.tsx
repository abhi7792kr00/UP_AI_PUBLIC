import { Navigate, Route, Routes } from "react-router-dom";

import { CitizenLayout } from "./layouts/CitizenLayout";
import { ProtectedRoute } from "./features/auth/guards/ProtectedRoute";
import { RoleGuard } from "./features/auth/guards/RoleGuard";

import { CitizenLogin } from "./pages/auth/CitizenLogin";

import CitizenDashboard from "./pages/citizen/CitizenDashboard";
import CitizenComplaints from "./pages/citizen/CitizenComplaints";
import CitizenComplaintDetails from "./pages/CitizenComplaintDetails";
import { NewComplaint } from "./pages/NewComplaint";
import CitizenProfile from "./pages/citizen/portal/CitizenProfile";
import CitizenDocuments from "./pages/citizen/portal/CitizenDocuments";
import CitizenNotifications from "./pages/citizen/portal/CitizenNotifications";
import CitizenAIAssistant from "./pages/citizen/portal/CitizenAIAssistant";
import CitizenVoiceAI from "./pages/citizen/portal/CitizenVoiceAI";
import CitizenSettings from "./pages/citizen/portal/CitizenSettings";

import { Unauthorized } from "./pages/Unauthorized";

export default function App() {
  return (
    <Routes>

      {/* =====================================================
          ONLY PUBLIC PAGE
      ====================================================== */}

      <Route
        path="/login/citizen"
        element={<CitizenLogin />}
      />


      {/* =====================================================
          AUTHENTICATED CITIZEN PORTAL
          role_id = 9
      ====================================================== */}

      <Route element={<ProtectedRoute />}>
        <Route element={<RoleGuard allowedRoles={[9]} />}>
          <Route element={<CitizenLayout />}>

            <Route
              path="/citizen"
              element={<CitizenDashboard />}
            />

            <Route
              path="/citizen/complaints"
              element={<CitizenComplaints />}
            />

            <Route
              path="/citizen/complaints/new"
              element={<NewComplaint />}
            />

            <Route
              path="/citizen/complaints/:complaintNumber"
              element={<CitizenComplaintDetails />}
            />

            <Route
  path="/citizen/profile"
  element={<CitizenProfile />}
/>

<Route
  path="/citizen/documents"
  element={<CitizenDocuments />}
/>

<Route
  path="/citizen/notifications"
  element={<CitizenNotifications />}
/>

<Route
  path="/ai"
  element={<CitizenAIAssistant />}
/>

<Route
  path="/citizen/voice"
  element={<CitizenVoiceAI />}
/>

<Route
  path="/citizen/settings"
  element={<CitizenSettings />}
/>
          </Route>
        </Route>
      </Route>


      {/* =====================================================
          AUTHORIZATION
      ====================================================== */}

      <Route
        path="/unauthorized"
        element={<Unauthorized />}
      />


      {/* =====================================================
          EVERYTHING ELSE → LOGIN
      ====================================================== */}

      <Route
        path="*"
        element={
          <Navigate
            to="/login/citizen"
            replace
          />
        }
      />

    </Routes>
  );
}
