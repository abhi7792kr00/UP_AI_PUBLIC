import {
  Sparkles,
  MessageCircle,
  Search,
  FileQuestion,
} from "lucide-react";

import "./citizen-portal.css";

export default function CitizenAIAssistant() {
  return (
    <div className="citizen-portal-page">
      <div className="citizen-portal-container">
        <div className="portal-header">
          <div className="portal-eyebrow">UP_AI</div>
          <h1 className="portal-title">AI Assistant</h1>
          <p className="portal-description">
            Get help understanding government services and citizen
            processes.
          </p>
        </div>

        <div className="ai-box">
          <Sparkles size={32} color="#7c3aed" />

          <h2>AI Citizen Assistant</h2>

          <p>
            The AI assistant interface is ready. The conversational AI
            backend can be connected here to answer citizen questions,
            explain services, and guide users through complaint-related
            processes.
          </p>
        </div>

        <div style={{ height: 18 }} />

        <div className="portal-feature-grid">
          <div className="portal-feature">
            <div className="portal-feature-icon">
              <MessageCircle size={20} />
            </div>

            <h3>Ask Questions</h3>

            <p>
              Ask questions about government services and citizen
              procedures.
            </p>
          </div>

          <div className="portal-feature">
            <div className="portal-feature-icon">
              <Search size={20} />
            </div>

            <h3>Find Services</h3>

            <p>
              Get guidance about the appropriate government service for
              your requirement.
            </p>
          </div>

          <div className="portal-feature">
            <div className="portal-feature-icon">
              <FileQuestion size={20} />
            </div>

            <h3>Understand Complaints</h3>

            <p>
              Get assistance understanding complaint status and required
              actions.
            </p>
          </div>
        </div>

        <div style={{ height: 18 }} />

        <div className="portal-card">
          <div className="portal-empty">
            <h3>AI backend connection pending</h3>

            <p>
              No AI API endpoint is being assumed until it is implemented
              in the backend.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
