import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import {
  CalendarDays,
  ChevronRight,
  Clock3,
  FileText,
  LoaderCircle,
  Plus,
} from "lucide-react";

import { useMyComplaints } from "../../features/citizen/hooks/useCitizenComplaints";
import { mapCitizenComplaint } from "../../features/citizen/utils/complaint-mapper";

import {
  useComplaintCategories,
  useDepartments,
  useComplaintStatuses,
} from "../../features/complaints/hooks/useComplaintMasterData";

export default function CitizenComplaints() {
  const navigate = useNavigate();

  const {
    data: complaints = [],
    isLoading,
    isError,
  } = useMyComplaints();

  const { data: categories = [] } =
    useComplaintCategories();

  const { data: departments = [] } =
    useDepartments();

  const { data: statuses = [] } =
    useComplaintStatuses();

  const mappedComplaints = useMemo(
    () =>
      complaints.map((complaint) =>
        mapCitizenComplaint(
          complaint,
          categories,
          departments,
          statuses,
        ),
      ),
    [
      complaints,
      categories,
      departments,
      statuses,
    ],
  );

  const total = mappedComplaints.length;

  const pending = mappedComplaints.filter(
    (item) => item.status === "Pending",
  ).length;

  const inProgress = mappedComplaints.filter(
    (item) => item.status === "In Progress",
  ).length;

  const resolved = mappedComplaints.filter(
    (item) => item.status === "Resolved",
  ).length;

  return (
    <main className="citizen-main">

      {/* =========================================
          PAGE HEADER
      ========================================== */}

      <section className="citizen-complaints-hero">

        <div className="citizen-complaints-hero-content">

          <span className="citizen-complaints-eyebrow">
            CITIZEN SERVICES
          </span>

          <h1>
            My Complaints
          </h1>

          <p>
            Apni sabhi registered complaints ko
            ek jagah manage karein aur unka
            latest status dekhein.
          </p>

        </div>

        <div className="citizen-complaints-hero-action">

          <button
            type="button"
            onClick={() =>
              navigate("/citizen/complaints/new")
            }
          >
            <Plus size={20} />
            New Complaint
          </button>

        </div>

      </section>


      {/* =========================================
          SUMMARY
      ========================================== */}

      <section className="citizen-complaint-summary">

        <div className="complaint-summary-card">
          <div className="summary-icon summary-total">
            <FileText size={22} />
          </div>

          <div>
            <span>Total</span>
            <strong>
              {isLoading ? "—" : total}
            </strong>
          </div>
        </div>

        <div className="complaint-summary-card">
          <div className="summary-icon summary-pending">
            <Clock3 size={22} />
          </div>

          <div>
            <span>Pending</span>
            <strong>
              {isLoading ? "—" : pending}
            </strong>
          </div>
        </div>

        <div className="complaint-summary-card">
          <div className="summary-icon summary-progress">
            <LoaderCircle size={22} />
          </div>

          <div>
            <span>In Progress</span>
            <strong>
              {isLoading ? "—" : inProgress}
            </strong>
          </div>
        </div>

        <div className="complaint-summary-card">
          <div className="summary-icon summary-resolved">
            <span>✓</span>
          </div>

          <div>
            <span>Resolved</span>
            <strong>
              {isLoading ? "—" : resolved}
            </strong>
          </div>
        </div>

      </section>


      {/* =========================================
          COMPLAINT LIST
      ========================================== */}

      <section className="citizen-complaints-panel">

        <div className="citizen-complaints-panel-header">

          <div>
            <span className="panel-eyebrow">
              COMPLAINT HISTORY
            </span>

            <h2>
              Your Complaints
            </h2>

            <p>
              Latest complaints are shown first.
            </p>
          </div>

          <div className="complaint-count">
            {total} Complaints
          </div>

        </div>


        {/* Loading */}

        {isLoading && (
          <div className="complaints-state">
            <LoaderCircle
              size={34}
              className="complaints-spinner"
            />

            <strong>
              Complaints load ho rahi hain...
            </strong>

            <span>
              Please wait.
            </span>
          </div>
        )}


        {/* Error */}

        {!isLoading && isError && (
          <div className="complaints-state complaints-error">
            <FileText size={38} />

            <strong>
              Complaints load nahi ho saki.
            </strong>

            <span>
              Backend connection check karke
              dobara try karein.
            </span>
          </div>
        )}


        {/* Empty */}

        {!isLoading &&
          !isError &&
          mappedComplaints.length === 0 && (
            <div className="complaints-state">

              <div className="empty-complaint-icon">
                <FileText size={40} />
              </div>

              <strong>
                Abhi koi complaint nahi hai.
              </strong>

              <span>
                Apni pehli complaint register karein.
              </span>

              <button
                type="button"
                onClick={() =>
                  navigate(
                    "/citizen/complaints/new",
                  )
                }
              >
                <Plus size={19} />
                Register Complaint
              </button>

            </div>
          )}


        {/* Ordered Complaint List */}

        {!isLoading &&
          !isError &&
          mappedComplaints.length > 0 && (
            <div className="citizen-complaint-list">

              {mappedComplaints.map(
                (complaint, index) => {

                  const statusModifier =
                    complaint.status ===
                    "Resolved"
                      ? "resolved"
                      : complaint.status ===
                          "Pending"
                        ? "pending"
                        : "progress";

                  return (
                    <button
                      key={
                        complaint.complaintNumber
                      }
                      type="button"
                      className="citizen-complaint-card"
                      onClick={() =>
                        navigate(
                          `/citizen/complaints/${encodeURIComponent(
                            complaint.complaintNumber,
                          )}`,
                        )
                      }
                    >

                      {/* Number */}

                      <div className="complaint-order">
                        <span>
                          {String(
                            index + 1,
                          ).padStart(2, "0")}
                        </span>
                      </div>


                      {/* Main Icon */}

                      <div className="complaint-card-icon">
                        <FileText size={23} />
                      </div>


                      {/* Content */}

                      <div className="complaint-card-content">

                        <div className="complaint-card-top">

                          <span className="complaint-number">
                            {complaint.complaintNumber}
                          </span>

                          <span
                            className={`complaint-status ${statusModifier}`}
                          >
                            <span className="status-dot" />
                            {complaint.status}
                          </span>

                        </div>

                        <h3>
                          {complaint.subject}
                        </h3>

                        <div className="complaint-card-meta">

                          <span>
                            {complaint.category}
                          </span>

                          <i />

                          <span>
                            {complaint.department}
                          </span>

                        </div>

                        <div className="complaint-card-date">
                          <CalendarDays size={15} />
                          Registered on{" "}
                          {complaint.date}
                        </div>

                      </div>


                      {/* Action */}

                      <div className="complaint-card-action">

                        <span>
                          View Details
                        </span>

                        <ChevronRight
                          size={22}
                        />

                      </div>

                    </button>
                  );
                },
              )}

            </div>
          )}

      </section>

    </main>
  );
}
