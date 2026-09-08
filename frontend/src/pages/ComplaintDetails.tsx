import {
  formatBackendDateTime,
} from "../utils/backend-date";

import { Link, useParams } from "react-router-dom";
import {
  ArrowLeft,
  Clock3,
  LoaderCircle,
  MapPin,
  MessageSquare,
  Paperclip,
  ShieldCheck,
} from "lucide-react";

import { Badge, Button, Card, PageHeader } from "../components/ui";
import {
  useMyComplaint,
} from "../features/citizen/hooks/useCitizenComplaints";
import {
  getComplaintTimeline,
  getComplaintFeedback,
} from "../features/citizen/api/citizen.api";
import { useQuery } from "@tanstack/react-query";

export function ComplaintDetails() {
  const { id: complaintNumber } = useParams();

  const complaintQuery = useMyComplaint(
    complaintNumber ?? "",
  );

  const timelineQuery = useQuery({
    queryKey: [
      "citizen",
      "complaint-timeline",
      complaintNumber,
    ],
    queryFn: () =>
      getComplaintTimeline(complaintNumber ?? ""),
    enabled: Boolean(complaintNumber),
  });

  const feedbackQuery = useQuery({
    queryKey: [
      "citizen",
      "complaint-feedback",
      complaintNumber,
    ],
    queryFn: () =>
      getComplaintFeedback(complaintNumber ?? ""),
    enabled: Boolean(complaintNumber),
  });

  if (complaintQuery.isLoading) {
    return (
      <div className="page">
        <div className="loading-state">
          <LoaderCircle className="animate-spin" size={24} />
          Loading complaint...
        </div>
      </div>
    );
  }

  if (complaintQuery.isError || !complaintQuery.data) {
    return (
      <div className="page">
        <Link
          className="back-link"
          to="/dashboard"
        >
          <ArrowLeft size={16} />
          Back to dashboard
        </Link>

        <Card>
          <h3>Complaint not found</h3>
          <p>
            This complaint could not be loaded from
            the server.
          </p>
        </Card>
      </div>
    );
  }

  const complaint = complaintQuery.data;
  const timeline = timelineQuery.data ?? [];

  return (
    <div className="page">
      <Link
        className="back-link"
        to="/dashboard"
      >
        <ArrowLeft size={16} />
        Back to dashboard
      </Link>

      <PageHeader
        eyebrow={complaint.complaint_number}
        title={complaint.subject}
        description={complaint.description}
      />

      <div className="details-layout">
        <div className="main-column">

          <Card>
            <div className="card-heading">
              <div>
                <h3>Complaint Information</h3>
                <p>
                  Information loaded directly from
                  UP_AI backend.
                </p>
              </div>

              <Badge tone="info">
                Status ID: {complaint.status_id}
              </Badge>
            </div>

            <div className="details-grid">
              <div>
                <small>Complaint Number</small>
                <strong>
                  {complaint.complaint_number}
                </strong>
              </div>

              <div>
                <small>Category ID</small>
                <strong>
                  {complaint.category_id}
                </strong>
              </div>

              <div>
                <small>Department ID</small>
                <strong>
                  {complaint.department_id ?? "Not assigned"}
                </strong>
              </div>

              <div>
                <small>District ID</small>
                <strong>
                  {complaint.district_id}
                </strong>
              </div>

              <div>
                <small>Created</small>
                <strong>
                  {new Date(
                    complaint.created_at,
                  ).toLocaleString("en-IN")}
                </strong>
              </div>

              <div>
                <small>Updated</small>
                <strong>
                  {new Date(
                    complaint.updated_at,
                  ).toLocaleString("en-IN")}
                </strong>
              </div>
            </div>
          </Card>

          <Card>
            <div className="card-heading">
              <div>
                <h3>Live Workflow</h3>
                <p>
                  Complete complaint workflow timeline.
                </p>
              </div>
            </div>

            {timelineQuery.isLoading && (
              <div className="loading-state">
                <LoaderCircle
                  className="animate-spin"
                  size={20}
                />
                Loading timeline...
              </div>
            )}

            {timelineQuery.isError && (
              <div className="evidence-empty">
                Timeline could not be loaded.
              </div>
            )}

            {!timelineQuery.isLoading &&
              !timelineQuery.isError &&
              timeline.length === 0 && (
                <div className="evidence-empty">
                  No workflow events recorded yet.
                </div>
              )}

            {timeline.length > 0 && (
              <div className="timeline">
                {timeline.map((event, index) => (
                  <div
                    className="timeline-item done"
                    key={event.id}
                  >
                    <div className="timeline-dot">
                      {index + 1}
                    </div>

                    <div className="timeline-content">
                      <div className="timeline-title">
                        <strong>
                          {event.action}
                        </strong>

                        <span>
                          {formatBackendDateTime(
                            event.created_at,
                          )}
                        </span>
                      </div>

                      {event.remarks && (
                        <p>{event.remarks}</p>
                      )}

                      <small>
                        Reference:{" "}
                        {event.reference_number}
                      </small>

                      {event.performed_by && (
                        <small>
                          Performed by user ID:{" "}
                          {event.performed_by}
                        </small>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>

          <Card>
            <div className="card-heading">
              <div>
                <h3>Evidence</h3>
                <p>
                  Documents and media associated with
                  this complaint.
                </p>
              </div>

              <Button
                variant="secondary"
                disabled
              >
                <Paperclip size={16} />
                Add evidence
              </Button>
            </div>

            {complaint.has_attachment ? (
              <div>
                Attachment is available for this
                complaint.
              </div>
            ) : (
              <div className="evidence-empty">
                No attachment uploaded.
              </div>
            )}
          </Card>
        </div>

        <aside className="details-side">

          <Card>
            <div className="side-title">
              <Clock3 size={19} />
              Complaint Status
            </div>

            <div className="big-number">
              #{complaint.status_id}
            </div>

            <small>
              Status is controlled by the backend
              workflow.
            </small>
          </Card>

          <Card>
            <div className="side-title">
              <MapPin size={19} />
              Location
            </div>

            <strong>
              {complaint.address ??
                "Address not provided"}
            </strong>

            <p>
              Pincode:{" "}
              {complaint.pincode ??
                "Not provided"}
            </p>

            {complaint.latitude !== null &&
              complaint.longitude !== null && (
                <small>
                  Coordinates:{" "}
                  {complaint.latitude},{" "}
                  {complaint.longitude}
                </small>
              )}
          </Card>

          <Card>
            <div className="side-title">
              <MessageSquare size={19} />
              Citizen Feedback
            </div>

            {feedbackQuery.isLoading && (
              <div className="loading-state">
                Loading feedback...
              </div>
            )}

            {!feedbackQuery.isLoading &&
              feedbackQuery.data && (
                <div>
                  <strong>
                    Rating:{" "}
                    {feedbackQuery.data.rating}/5
                  </strong>

                  {feedbackQuery.data.feedback_text && (
                    <p>
                      {feedbackQuery.data.feedback_text}
                    </p>
                  )}
                </div>
              )}

            {!feedbackQuery.isLoading &&
              !feedbackQuery.data && (
                <p>
                  Feedback has not been submitted yet.
                </p>
              )}

            <Button
              variant="secondary"
              disabled
            >
              Give feedback
            </Button>
          </Card>

          <Card>
            <div className="side-title">
              <ShieldCheck size={19} />
              Audit Ready
            </div>

            <p>
              Complaint actions, timestamps and
              workflow responsibility are loaded from
              the backend.
            </p>
          </Card>

        </aside>
      </div>
    </div>
  );
}
