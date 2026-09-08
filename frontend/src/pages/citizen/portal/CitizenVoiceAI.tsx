import {
  Mic,
  Volume2,
  MessageSquareText,
} from "lucide-react";

import "./citizen-portal.css";

export default function CitizenVoiceAI() {
  return (
    <div className="citizen-portal-page">
      <div className="citizen-portal-container">
        <div className="portal-header">
          <div className="portal-eyebrow">UP_AI Voice</div>
          <h1 className="portal-title">Voice AI</h1>
          <p className="portal-description">
            Interact with citizen services using voice.
          </p>
        </div>

        <div className="portal-card">
          <div style={{ textAlign: "center" }}>
            <div className="voice-circle">
              <Mic size={38} />
            </div>

            <h2 style={{ margin: "0 0 8px" }}>
              Voice Assistant
            </h2>

            <p className="portal-description">
              Voice interaction is ready for backend integration.
            </p>

            <div style={{ marginTop: 18 }}>
              <span className="portal-status">
                Backend connection pending
              </span>
            </div>
          </div>
        </div>

        <div style={{ height: 18 }} />

        <div className="portal-feature-grid">
          <div className="portal-feature">
            <div className="portal-feature-icon">
              <Mic size={20} />
            </div>

            <h3>Voice Input</h3>

            <p>
              Citizens will be able to ask questions using their voice.
            </p>
          </div>

          <div className="portal-feature">
            <div className="portal-feature-icon">
              <Volume2 size={20} />
            </div>

            <h3>Voice Response</h3>

            <p>
              AI responses can be converted into spoken answers.
            </p>
          </div>

          <div className="portal-feature">
            <div className="portal-feature-icon">
              <MessageSquareText size={20} />
            </div>

            <h3>Citizen Assistance</h3>

            <p>
              Voice AI can guide citizens through available services.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
