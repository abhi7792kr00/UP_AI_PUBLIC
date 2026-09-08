import { Link } from "react-router-dom";

export function Unauthorized() {
  return (
    <div
      style={{
        minHeight: "100vh",
        display: "grid",
        placeItems: "center",
        padding: "24px",
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h1>Access Denied</h1>

        <p>
          You do not have permission to access this portal.
        </p>

        <Link to="/">
          Go to Home
        </Link>
      </div>
    </div>
  );
}
