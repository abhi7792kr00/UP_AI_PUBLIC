import { useEffect, useState } from "react";
import {
  Settings,
  Bell,
  Globe2,
  ShieldCheck,
  Sun,
  Moon,
  Monitor,
  Check,
} from "lucide-react";

import {
  applyCitizenTheme,
  getCitizenTheme,
  type CitizenTheme,
} from "../../../theme/citizenTheme";

import "./citizen-portal.css";

const themeOptions: {
  value: CitizenTheme;
  title: string;
  description: string;
  icon: typeof Sun;
}[] = [
  {
    value: "light",
    title: "Light",
    description: "Use the bright Citizen Portal interface.",
    icon: Sun,
  },
  {
    value: "dark",
    title: "Dark",
    description: "Use a dark interface that is easier on the eyes.",
    icon: Moon,
  },
  {
    value: "system",
    title: "System",
    description: "Automatically follow your device preference.",
    icon: Monitor,
  },
];

export default function CitizenSettings() {
  const [theme, setTheme] =
    useState<CitizenTheme>("system");

  const [notifications, setNotifications] =
    useState(true);

  const [securityAlerts, setSecurityAlerts] =
    useState(true);

  useEffect(() => {
    setTheme(getCitizenTheme());
  }, []);

  const handleThemeChange = (value: CitizenTheme) => {
    setTheme(value);
    applyCitizenTheme(value);
  };

  return (
    <div className="citizen-portal-page">
      <div className="citizen-portal-container">
        <div className="portal-header">
          <div className="portal-eyebrow">
            Preferences
          </div>

          <h1 className="portal-title">
            Settings
          </h1>

          <p className="portal-description">
            Manage your Citizen Portal preferences.
          </p>
        </div>

        {/* APPEARANCE */}

        <div className="portal-card">
          <h2 className="portal-card-title">
            <Settings size={19} />
            Appearance
          </h2>

          <div className="theme-option-grid">
            {themeOptions.map((option) => {
              const Icon = option.icon;
              const selected = theme === option.value;

              return (
                <button
                  key={option.value}
                  type="button"
                  className={`theme-option ${
                    selected ? "selected" : ""
                  }`}
                  onClick={() =>
                    handleThemeChange(option.value)
                  }
                >
                  <div className="theme-option-icon">
                    <Icon size={21} />
                  </div>

                  <div className="theme-option-content">
                    <strong>
                      {option.title}
                    </strong>

                    <span>
                      {option.description}
                    </span>
                  </div>

                  {selected && (
                    <div className="theme-option-check">
                      <Check size={16} />
                    </div>
                  )}
                </button>
              );
            })}
          </div>
        </div>

        <div style={{ height: 18 }} />

        {/* NOTIFICATIONS */}

        <div className="portal-card">
          <h2 className="portal-card-title">
            <Bell size={19} />
            Notifications
          </h2>

          <div className="portal-setting">
            <div>
              <h3>Complaint Notifications</h3>

              <p>
                Receive updates when your complaint
                status changes.
              </p>
            </div>

            <button
              type="button"
              aria-label="Toggle complaint notifications"
              className={`portal-toggle ${
                notifications ? "active" : ""
              }`}
              onClick={() =>
                setNotifications(
                  (value) => !value,
                )
              }
            />
          </div>

          <div className="portal-setting">
            <div>
              <h3>Security Alerts</h3>

              <p>
                Receive important security-related
                account alerts.
              </p>
            </div>

            <button
              type="button"
              aria-label="Toggle security alerts"
              className={`portal-toggle ${
                securityAlerts ? "active" : ""
              }`}
              onClick={() =>
                setSecurityAlerts(
                  (value) => !value,
                )
              }
            />
          </div>
        </div>

        <div style={{ height: 18 }} />

        {/* LANGUAGE */}

        <div className="portal-card">
          <h2 className="portal-card-title">
            <Globe2 size={19} />
            Language
          </h2>

          <div className="portal-setting">
            <div>
              <h3>Portal Language</h3>

              <p>
                Change the portal language using the
                language selector in the top bar.
              </p>
            </div>

            <Globe2
              size={22}
              color="#7c3aed"
            />
          </div>
        </div>

        <div style={{ height: 18 }} />

        {/* SECURITY */}

        <div className="portal-card">
          <h2 className="portal-card-title">
            <ShieldCheck size={19} />
            Account Security
          </h2>

          <div className="portal-setting">
            <div>
              <h3>Authenticated Session</h3>

              <p>
                Your Citizen Portal session is protected
                by authenticated access.
              </p>
            </div>

            <ShieldCheck
              size={22}
              color="#7c3aed"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
