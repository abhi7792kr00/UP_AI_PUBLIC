import {
  Bell,
  CheckCircle2,
  Info,
  Clock3,
} from "lucide-react";

import "./citizen-portal.css";

export default function CitizenNotifications() {
  return (
    <div className="citizen-portal-page">
      <div className="citizen-portal-container">
        <div className="portal-header">
          <div className="portal-eyebrow">Updates</div>
          <h1 className="portal-title">Notifications</h1>
          <p className="portal-description">
            Stay informed about complaints and citizen services.
          </p>
        </div>

        <div className="portal-card">
          <div className="portal-empty">
            <div className="portal-empty-icon">
              <Bell size={25} />
            </div>

            <h3>No notifications yet</h3>

            <p>
              Notification data will appear here when the notification
              service is connected to the portal.
            </p>
          </div>
        </div>

        <div style={{ height: 18 }} />

        <div className="portal-feature-grid">
          <div className="portal-feature">
            <div className="portal-feature-icon">
              <CheckCircle2 size={20} />
            </div>

            <h3>Complaint Updates</h3>

            <p>
              Get notified when the status of your complaint changes.
            </p>
          </div>

          <div className="portal-feature">
            <div className="portal-feature-icon">
              <Info size={20} />
            </div>

            <h3>Service Updates</h3>

            <p>
              Receive important updates related to citizen services.
            </p>
          </div>

          <div className="portal-feature">
            <div className="portal-feature-icon">
              <Clock3 size={20} />
            </div>

            <h3>Pending Actions</h3>

            <p>
              Important actions requiring your attention can appear here.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
