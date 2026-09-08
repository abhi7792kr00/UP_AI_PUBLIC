import {
  FileText,
  Upload,
  FolderOpen,
  ShieldCheck,
} from "lucide-react";

import "./citizen-portal.css";

export default function CitizenDocuments() {
  return (
    <div className="citizen-portal-page">
      <div className="citizen-portal-container">
        <div className="portal-header">
          <div className="portal-eyebrow">Citizen Services</div>
          <h1 className="portal-title">My Documents</h1>
          <p className="portal-description">
            Manage documents associated with your citizen services.
          </p>
        </div>

        <div className="portal-card">
          <div className="portal-empty">
            <div className="portal-empty-icon">
              <FolderOpen size={25} />
            </div>

            <h3>Document service is coming soon</h3>

            <p>
              The document management backend is not connected to the
              Citizen Portal yet.
            </p>
          </div>
        </div>

        <div style={{ height: 18 }} />

        <div className="portal-feature-grid">
          <div className="portal-feature">
            <div className="portal-feature-icon">
              <FileText size={20} />
            </div>

            <h3>View Documents</h3>

            <p>
              View documents submitted with government services and
              complaints.
            </p>
          </div>

          <div className="portal-feature">
            <div className="portal-feature-icon">
              <Upload size={20} />
            </div>

            <h3>Upload Documents</h3>

            <p>
              Upload supporting documents when a connected service
              requires them.
            </p>
          </div>

          <div className="portal-feature">
            <div className="portal-feature-icon">
              <ShieldCheck size={20} />
            </div>

            <h3>Secure Storage</h3>

            <p>
              Documents will be associated with your authenticated citizen
              account.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}