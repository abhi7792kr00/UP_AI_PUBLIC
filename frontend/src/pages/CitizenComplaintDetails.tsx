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
  ShieldCheck,
} from "lucide-react";

import { Card, PageHeader } from "../components/ui";
import {
  useMyComplaintDetails,
  useMyComplaintTimeline,
} from "../features/citizen/hooks/useCitizenComplaintDetails";

export function CitizenComplaintDetails() {
  const { complaintNumber = "" } = useParams<{
    complaintNumber: string;
  }>();

  const complaintQuery =
    useMyComplaintDetails(complaintNumber);

  const timelineQuery =
    useMyComplaintTimeline(complaintNumber);

  if (complaintQuery.isLoading) {
    return (
      <div className="page">
        <Card>
          <LoaderCircle size={24} className="spin" />
          Loading complaint...
        </Card>
      </div>
    );
  }

  if (complaintQuery.isError || !complaintQuery.data) {
    return (
      <div className="page">
        <PageHeader
          eyebrow="CITIZEN"
          title="Complaint not found"
        />

        <Card>
          <p>
            Unable to load complaint{" "}
            <strong>{complaintNumber}</strong>.
          </p>

          <Link
            className="btn btn-secondary"
            to="/citizen"
          >
            <ArrowLeft size={17} />
            Back to Dashboard
          </Link>
        </Card>
      </div>
    );
  }

  const complaint = complaintQuery.data;

  return (
    <div className="page">
      <PageHeader
        eyebrow="CITIZEN COMPLAINT"
        title={complaint.subject}
        description={`Complaint No. ${complaint.complaint_number}`}
        action={
          <Link
            className="btn btn-secondary"
            to="/citizen"
          >
            <ArrowLeft size={17} />
            Dashboard
          </Link>
        }
      />

      <div className="dashboard-grid">
        <Card>
          <div className="card-heading">
            <ShieldCheck size={20} />
            <div>
              <strong>Complaint Information</strong>
              <span>
                Backend-generated complaint record
              </span>
            </div>
          </div>

          <div className="detail-list">
            <div>
              <span>Complaint Number</span>
              <strong>
                {complaint.complaint_number}
              </strong>
            </div>

            <div>
              <span>Subject</span>
              <strong>{complaint.subject}</strong>
            </div>

            <div>
              <span>Description</span>
              <strong>{complaint.description}</strong>
            </div>

            <div>
              <span>Status ID</span>
              <strong>{complaint.status_id}</strong>
            </div>

            <div>
              <span>Category ID</span>
              <strong>{complaint.category_id}</strong>
            </div>

            <div>
              <span>Department ID</span>
              <strong>
                {complaint.department_id ?? "Not assigned"}
              </strong>
            </div>

            <div>
              <span>
                <MapPin size={16} />
                Address
              </span>
              <strong>
                {complaint.address ?? "Not provided"}
              </strong>
            </div>

            <div>
              <span>Created</span>
              <strong>
                {formatBackendDateTime(
                  complaint.created_at,
                )}
              </strong>
            </div>
          </div>
        </Card>

        <Card>
          <div className="card-heading">
            <Clock3 size={20} />
            <div>
              <strong>Complaint Timeline</strong>
              <span>
                Real workflow history from backend
              </span>
            </div>
          </div>

          {timelineQuery.isLoading && (
            <div>
              <LoaderCircle size={22} className="spin" />
              Loading timeline...
            </div>
          )}

          {timelineQuery.isError && (
            <p>
              Timeline could not be loaded.
            </p>
          )}

          {!timelineQuery.isLoading &&
            !timelineQuery.isError &&
            timelineQuery.data?.length === 0 && (
              <p>
                No timeline activity available yet.
              </p>
            )}

          <div className="timeline">
            {timelineQuery.data?.map((item) => (
              <div
                className="timeline-item"
                key={item.id}
              >
                <div className="timeline-dot" />

                <div>
                  <strong>{item.action}</strong>

                  {item.remarks && (
                    <p>{item.remarks}</p>
                  )}

                  <small>
                    {formatBackendDateTime(
                      item.created_at,
                    )}
                  </small>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <Card>
        <div className="card-heading">
          <MessageSquare size={20} />
          <div>
            <strong>Citizen Information</strong>
            <span>
              Information associated with this complaint
            </span>
          </div>
        </div>

        <div className="detail-list">
          <div>
            <span>Mobile</span>
            <strong>
              {complaint.mobile_number ?? "Not provided"}
            </strong>
          </div>

          <div>
            <span>Email</span>
            <strong>
              {complaint.email ?? "Not provided"}
            </strong>
          </div>

          <div>
            <span>Pincode</span>
            <strong>
              {complaint.pincode ?? "Not provided"}
            </strong>
          </div>
        </div>
      </Card>
    </div>
  );
}

export default CitizenComplaintDetails;
