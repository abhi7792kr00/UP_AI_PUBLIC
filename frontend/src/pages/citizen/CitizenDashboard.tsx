import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Bell,
  Bot,
  Building2,
  ChevronDown,
  ChevronRight,
  CircleHelp,
  FileText,
  Globe2,
  Home,
  LogOut,
  Menu,
  Mic,
  Plus,
  Search,
  Settings,
  ShieldCheck,
  UserRound,
  Users,
  X,
  Zap,
  CheckCircle2,
  Clock3,
  LoaderCircle,
  MapPin,
} from "lucide-react";

import "./citizen-dashboard.css";

import {
  formatBackendDate,
  parseBackendDate,
} from "../../utils/backend-date";
import { getCitizenTranslations } from "../../i18n/citizenTranslations";

import { useMyComplaints } from "../../features/citizen/hooks/useCitizenComplaints";
import { useMyComplaintTimeline } from "../../features/citizen/hooks/useCitizenComplaintDetails";
import { useLogout } from "../../features/auth/hooks/useLogout";
import { mapCitizenComplaint } from "../../features/citizen/utils/complaint-mapper";

import {
  useComplaintCategories,
  useDepartments,
  useComplaintStatuses,
} from "../../features/complaints/hooks/useComplaintMasterData";

import {
  useDistricts,
  useTehsils,
  useBlocks,
  useMunicipalBodies,
  useWards,
  useLocalities,
  useGovernmentDepartments,
  useDesignations,
  useOffices,
  useGovernmentOfficers,
} from "../../features/government/hooks/useGovernmentData";

import type {
  District,
  Tehsil,
  GovernmentDepartment,
  Designation,
  Office,
  Officer,
} from "../../features/government/api/government.api";

export type CitizenDashboardUser = {
  fullName: string;
  roleLabel?: string;
  avatarUrl?: string;
  preferredLanguage?: "Hindi" | "English";
};

export type CitizenDashboardOfficer = {
  id: number;
  officerName: string;
  photoUrl?: string | null;
  mobile?: string | null;
  email?: string | null;
  designationName?: string | null;
  departmentName?: string | null;
  officeName?: string | null;
};

export type CitizenDashboardComplaint = {
  complaintNumber: string;
  subject: string;
  category: string;
  department: string;
  status: "In Progress" | "Resolved" | "Pending";
  date: string;
  createdAt: string;

  assignedOfficer?: CitizenDashboardOfficer | null;

  icon?: "electricity" | "road" | "water" | "revenue" | "health";
};

export type CitizenNotification = {
  id: string | number;
  title: string;
  time: string;
  tone: "blue" | "orange" | "green";
  unread?: boolean;
};

export type CitizenDashboardProps = {
  user?: CitizenDashboardUser;
  notifications?: CitizenNotification[];

  onNewComplaint?: () => void;
  onTrackComplaint?: (complaintNumber: string) => void;
  onOpenAI?: () => void;
  onOpenVoiceAI?: () => void;
  onLogout?: () => void;
};

const DEFAULT_USER: CitizenDashboardUser = {
  fullName: "Citizen",
  roleLabel: "Citizen",
  preferredLanguage: "Hindi",
};

const DEFAULT_NOTIFICATIONS: CitizenNotification[] = [];

function complaintIcon(
  icon: CitizenDashboardComplaint["icon"],
) {
  const common = {
    size: 20,
    strokeWidth: 2,
  };

  switch (icon) {
    case "electricity":
      return <Zap {...common} />;

    case "road":
      return <Building2 {...common} />;

    case "water":
      return (
        <span className="citizen-dashboard-emoji">
          💧
        </span>
      );

    case "revenue":
      return <Building2 {...common} />;

    case "health":
      return (
        <span className="citizen-dashboard-emoji">
          ✚
        </span>
      );

    default:
      return <FileText {...common} />;
  }
}

function statusClass(
  status: CitizenDashboardComplaint["status"],
) {
  if (status === "Resolved") {
    return "status-resolved";
  }

  if (status === "Pending") {
    return "status-pending";
  }

  return "status-progress";
}

export function CitizenDashboard({
  user = DEFAULT_USER,
  notifications = DEFAULT_NOTIFICATIONS,
  onNewComplaint,
  onTrackComplaint,
  onOpenAI,
  onOpenVoiceAI,
  onLogout,
}: CitizenDashboardProps) {
  const logout = useLogout();
  const navigate = useNavigate();

  const handleNewComplaint = () => {
    navigate("/citizen/complaints/new");
    setSidebarOpen(false);
  };
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [language, setLanguage] = useState(
    user.preferredLanguage ?? "Hindi",
  );
  const [showNotifications, setShowNotifications] =
    useState(false);

  /*
   * ==============================
   * REAL BACKEND DATA
   * ==============================
   */

  const {
    data: apiComplaints,
    isLoading: complaintsLoading,
    isError: complaintsError,
  } = useMyComplaints();

  const {
    data: categories = [],
  } = useComplaintCategories();

  const {
    data: departments = [],
  } = useDepartments();

  const {
    data: statuses = [],
  } = useComplaintStatuses();

  /*
   * ==============================
   * GOVERNMENT DIRECTORY DATA
   * ==============================
   */

  const {
    data: districts = [],
    isLoading: districtsLoading,
  } = useDistricts();

  const {
    data: tehsils = [],
    isLoading: tehsilsLoading,
  } = useTehsils();

  const {
    data: blocks = [],
  } = useBlocks();

  const {
    data: municipalBodies = [],
  } = useMunicipalBodies();

  const {
    data: wards = [],
  } = useWards();

  const {
    data: localities = [],
  } = useLocalities();


  const {
    data: governmentDepartments = [],
    isLoading: departmentsLoading,
  } = useGovernmentDepartments();

  const {
    data: designations = [],
  } = useDesignations();

  const {
    data: offices = [],
  } = useOffices();

  const {
    data: governmentOfficers = [],
    isLoading: officersLoading,
  } = useGovernmentOfficers();

  const [selectedDistrictId, setSelectedDistrictId] =
    useState<number | "">("");

  const [selectedTehsilId, setSelectedTehsilId] =
    useState<number | "">("");

  const [selectedDepartmentId, setSelectedDepartmentId] =
    useState<number | "">("");

  const [selectedBlockId, setSelectedBlockId] =
    useState<number | "">("");

  const [selectedAreaType, setSelectedAreaType] =
    useState<"rural" | "urban">("rural");

  const [selectedMunicipalBodyId, setSelectedMunicipalBodyId] =
    useState<number | "">("");

  const [selectedWardId, setSelectedWardId] =
    useState<number | "">("");

  const [selectedLocalityId, setSelectedLocalityId] =
    useState<number | "">("");

  /*
   * ==============================
   * GOVERNMENT FILTERED DATA
   * ==============================
   */

  const filteredTehsils = useMemo(
    () =>
      selectedDistrictId === ""
        ? []
        : tehsils.filter(
            (tehsil) =>
              tehsil.district_id === selectedDistrictId,
          ),
    [tehsils, selectedDistrictId],
  );

  const filteredBlocks = useMemo(
    () =>
      selectedTehsilId === ""
        ? []
        : blocks.filter(
            (block) =>
              block.tehsil_ids.includes(selectedTehsilId),
          ),
    [blocks, selectedTehsilId],
  );

  const filteredMunicipalBodies = useMemo(
    () =>
      selectedDistrictId === ""
        ? []
        : municipalBodies.filter(
            (body) =>
              body.district_id === selectedDistrictId &&
              body.is_active !== false,
          ),
    [municipalBodies, selectedDistrictId],
  );

  const filteredWards = useMemo(
    () =>
      selectedMunicipalBodyId === ""
        ? []
        : wards.filter(
            (ward) =>
              ward.municipal_body_id ===
                selectedMunicipalBodyId &&
              ward.is_active !== false,
          ),
    [wards, selectedMunicipalBodyId],
  );

  const filteredLocalities = useMemo(
    () =>
      selectedWardId === ""
        ? []
        : localities.filter(
            (locality) =>
              locality.ward_id === selectedWardId &&
              locality.is_active !== false,
          ),
    [localities, selectedWardId],
  );

  const filteredOfficers = useMemo(
    () =>
      governmentOfficers.filter((officer) => {
        const departmentMatches =
          selectedDepartmentId === "" ||
          officer.department_id === selectedDepartmentId;

        if (!departmentMatches) {
          return false;
        }

        /*
         * Officer belongs to an Office.
         * Office is now geographically mapped to:
         * District → Tehsil → Block.
         */

        const office =
          offices.find(
            (item) =>
              item.id === officer.office_id,
          );

        if (!office) {
          return false;
        }

        const districtMatches =
          selectedDistrictId === "" ||
          office.district_id === selectedDistrictId;

        if (!districtMatches) {
          return false;
        }

        if (selectedAreaType === "rural") {
          const tehsilMatches =
            selectedTehsilId === "" ||
            office.tehsil_id === selectedTehsilId;

          const blockMatches =
            selectedBlockId === "" ||
            office.block_id === selectedBlockId;

          return (
            tehsilMatches &&
            blockMatches
          );
        }

        const municipalBodyMatches =
          selectedMunicipalBodyId === "" ||
          office.municipal_body_id ===
            selectedMunicipalBodyId;

        const wardMatches =
          selectedWardId === "" ||
          office.ward_id === selectedWardId;

        const localityMatches =
          selectedLocalityId === "" ||
          office.locality_id === selectedLocalityId;

        return (
          municipalBodyMatches &&
          wardMatches &&
          localityMatches
        );
      }),
    [
      governmentOfficers,
      offices,
      selectedDistrictId,
      selectedTehsilId,
      selectedBlockId,
      selectedDepartmentId,
    ],
  );

  /*
   * Backend complaints contain IDs.
   *
   * Dashboard requires human-readable:
   * category
   * department
   * status
   *
   * Mapper converts API response into dashboard data.
   */

  const realComplaints = useMemo<CitizenDashboardComplaint[]>(
    () =>
      (apiComplaints ?? []).map((complaint) =>
        mapCitizenComplaint(
          complaint,
          categories,
          departments,
          statuses,
        ),
      ),
    [
      apiComplaints,
      categories,
      departments,
      statuses,
    ],
  );

  /*
   * ==============================
   * RECENT COMPLAINTS
   * ==============================
   *
   * Only the current citizen's complaints
   * are already provided by useMyComplaints().
   *
   * Sort by actual backend creation timestamp
   * and show only the latest two.
   */

  const recentComplaints = useMemo(
    () =>
      [...realComplaints]
        .sort(
          (a, b) =>
            parseBackendDate(b.createdAt).getTime() -
            parseBackendDate(a.createdAt).getTime(),
        )
        .slice(0, 2),
    [realComplaints],
  );

  const recentComplaintNumber1 =
    recentComplaints[0]?.complaintNumber ?? "";

  const recentComplaintNumber2 =
    recentComplaints[1]?.complaintNumber ?? "";

  const recentTimeline1 = useMyComplaintTimeline(
    recentComplaintNumber1,
  );

  const recentTimeline2 = useMyComplaintTimeline(
    recentComplaintNumber2,
  );

  const recentComplaintTimelines = [
    recentTimeline1.data ?? [],
    recentTimeline2.data ?? [],
  ];

  /*
   * ==============================
   * DASHBOARD STATISTICS
   * ==============================
   */

  const stats = useMemo(() => {
    const total = realComplaints.length;

    const pending = realComplaints.filter(
      (complaint) =>
        complaint.status === "Pending",
    ).length;

    const inProgress = realComplaints.filter(
      (complaint) =>
        complaint.status === "In Progress",
    ).length;

    const resolved = realComplaints.filter(
      (complaint) =>
        complaint.status === "Resolved",
    ).length;

    return {
      total,
      pending,
      inProgress,
      resolved,
    };
  }, [realComplaints]);

  const unreadCount = notifications.filter(
    (notification) => notification.unread,
  ).length;

  return (
      <main className="citizen-main">

        {/* Welcome */}

        <section className="citizen-welcome">

          <div className="citizen-welcome-copy">

            <h1>
              Namaste, {user.fullName}{" "}
              <span>👋</span>
            </h1>

            <h2>
              Aapki sevaon mein hum aapke saath.
            </h2>

            <p>
              Uttar Pradesh ki behtar aur digital
              sarkar ke liye aapka yogdaan
              mahatvapurn hai.
            </p>

          </div>

          <div
            className="citizen-welcome-art"
            aria-hidden="true"
          >
            <div className="art-dome">
              ♜
            </div>

            <div className="art-building">
              ✦
            </div>

            <div className="art-building small">
              ♜
            </div>
          </div>

        </section>

        {/* =========================================
            CONTENT GRID
        ========================================== */}

        <section className="citizen-content-grid">

          <div className="citizen-primary-column">

            {/* =====================================
                STATISTICS
            ====================================== */}

            <section className="citizen-stat-grid">

              <article className="citizen-stat-card">

                <div className="stat-icon stat-blue">
                  <FileText size={24} />
                </div>

                <div>
                  <span>
                    Total Complaints
                  </span>

                  <strong>
                    {complaintsLoading
                      ? "—"
                      : stats.total}
                  </strong>

                  <small>
                    Aap dwara darj ki gayi
                    shikayatein
                  </small>
                </div>

              </article>

              <article className="citizen-stat-card">

                <div className="stat-icon stat-orange">
                  <Clock3 size={25} />
                </div>

                <div>
                  <span>Pending</span>

                  <strong>
                    {complaintsLoading
                      ? "—"
                      : stats.pending}
                  </strong>

                  <small>
                    Prarambhik star par
                  </small>
                </div>

              </article>

              <article className="citizen-stat-card">

                <div className="stat-icon stat-blue">
                  <LoaderCircle size={25} />
                </div>

                <div>
                  <span>In Progress</span>

                  <strong>
                    {complaintsLoading
                      ? "—"
                      : stats.inProgress}
                  </strong>

                  <small>
                    Karyavahi jaari hai
                  </small>
                </div>

              </article>

              <article className="citizen-stat-card">

                <div className="stat-icon stat-green">
                  <CheckCircle2 size={25} />
                </div>

                <div>
                  <span>Resolved</span>

                  <strong>
                    {complaintsLoading
                      ? "—"
                      : stats.resolved}
                  </strong>

                  <small>
                    Safalta se niptaayi gayi
                  </small>
                </div>

              </article>

            </section>

            {/* =====================================
                ACTIONS
            ====================================== */}

            <section className="citizen-action-row">


              <button
                className="citizen-secondary-action"
                type="button"
                onClick={onOpenAI}
              >
                <Bot size={23} />
                <span>
                  AI Assistant
                </span>
              </button>

              <button
                className="citizen-secondary-action"
                type="button"
                onClick={onOpenVoiceAI}
              >
                <Mic size={23} />
                <span>
                  Voice Assistant
                </span>
              </button>

            </section>

            {/* =====================================
                COMPLAINTS
            ====================================== */}

            <section
              className="citizen-card complaints-card"
              id="complaints"
            >

              <div className="citizen-section-heading">

                <div>
                  <h2>
                    <FileText size={23} />
                    Recent Complaints
                  </h2>
                </div>

                <button
                  type="button"
                  onClick={() =>
                    document
                      .getElementById(
                        "complaints",
                      )
                      ?.scrollIntoView({
                        behavior: "smooth",
                      })
                  }
                >
                  View All
                  <ChevronRight size={17} />
                </button>

              </div>

              {/* Loading */}

              {complaintsLoading && (
                <div className="citizen-empty-state">

                  <LoaderCircle
                    size={25}
                    className="animate-spin"
                  />

                  <span>
                    Complaints loading...
                  </span>

                </div>
              )}

              {/* Error */}

              {!complaintsLoading &&
                complaintsError && (
                  <div className="citizen-empty-state">

                    <FileText size={25} />

                    <span>
                      Complaints load nahi
                      ho paayi.
                    </span>

                    <button
                      type="button"
                      onClick={() =>
                        window.location.reload()
                      }
                    >
                      Retry
                    </button>

                  </div>
                )}

              {/* Empty */}

              {!complaintsLoading &&
                !complaintsError &&
                realComplaints.length === 0 && (
                  <div className="citizen-empty-state">

                    <FileText size={25} />

                    <span>
                      Abhi koi complaint
                      nahi hai.
                    </span>

                    
                  </div>
                )}

              {/* Recent Complaints with Timeline */}

              {!complaintsLoading &&
                !complaintsError &&
                realComplaints.length > 0 && (
                  <div className="complaints-timeline-list">

                    {recentComplaints.map(
                      (complaint, complaintIndex) => {
                        const timeline =
                          recentComplaintTimelines[
                            complaintIndex
                          ] ?? [];

                        const timelineText =
                          timeline.map(
                            (item) =>
                              `${item.action ?? ""} ${item.remarks ?? ""}`,
                          );

                        const hasAction = (
                          keywords: string[],
                        ) =>
                          timelineText.some((value) =>
                            keywords.some((keyword) =>
                              value
                                .toLowerCase()
                                .includes(keyword),
                            ),
                          );

                        const submitted =
                          hasAction([
                            "submit",
                            "created",
                            "register",
                          ]);

                        const registered =
                          hasAction([
                            "register",
                          ]);

                        const assignedDepartment =
                          hasAction([
                            "assign_department",
                            "assigned_department",
                            "department",
                            "dept",
                          ]);

                        const assignedOfficerFromTimeline =
                          hasAction([
                            "assign_complaint",
                            "assigned",
                            "officer",
                          ]);

                        const resolved =
                          complaint.status === "Resolved" ||
                          hasAction([
                            "resolve",
                            "closed",
                            "complete",
                          ]);

                        const inProgress =
                          complaint.status === "In Progress" ||
                          hasAction([
                            "investigation",
                            "progress",
                            "processing",
                            "restart",
                            "resume",
                          ]);

                        const steps = [
                          {
                            label: "Submitted",
                            active: true,
                          },
                          {
                            label: "Registered",
                            active:
                              registered ||
                              timeline.length === 0,
                          },
                          {
                            label: "Assigned to Dept.",
                            active: assignedDepartment,
                          },
                          {
                            label: "Assigned to Officer",
                            active:
                              assignedOfficerFromTimeline,
                          },
                          {
                            label:
                              resolved
                                ? "Resolved"
                                : inProgress
                                  ? "In Progress"
                                  : "Pending",
                            active:
                              resolved ||
                              inProgress,
                          },
                        ];

                        const formatTimelineDate = (
                          value?: string | null,
                        ) => {
                          if (!value) return "";

                          const date = new Date(value);

                          if (
                            Number.isNaN(
                              date.getTime(),
                            )
                          ) {
                            return "";
                          }

                          return formatBackendDate(
                            value,
                          );
                        };

                        const timelineDateFor =
                          (index: number) => {
                            const item =
                              timeline[index];

                            if (item?.created_at) {
                              return formatTimelineDate(
                                item.created_at,
                              );
                            }

                            if (index === 0) {
                              return complaint.date;
                            }

                            return "";
                          };

                        return (
                          <article
                            key={
                              complaint.complaintNumber
                            }
                            className="complaint-timeline-card"
                          >

                            {/* Complaint Summary */}

                            <div className="complaint-timeline-summary">

                              <div className="complaint-summary-top">

                                <div className="complaint-summary-title">

                                  <strong>
                                    {
                                      complaint.complaintNumber
                                    }
                                  </strong>

                                  <span
                                    className={`complaint-category-icon ${
                                      complaint.icon ??
                                      "default"
                                    }`}
                                  >
                                    {complaintIcon(
                                      complaint.icon,
                                    )}
                                  </span>

                                  <span className="complaint-timeline-category">
                                    {complaint.category}
                                  </span>

                                  <span
                                    className={`complaint-status ${statusClass(
                                      complaint.status,
                                    )}`}
                                  >
                                    <i />
                                    {complaint.status}
                                  </span>

                                </div>

                              </div>

                              <div className="complaint-summary-meta">

                                <span>
                                  {
                                    complaint.department
                                  }
                                </span>

                                <span className="complaint-meta-dot">
                                  •
                                </span>

                                <span>
                                  {complaint.date}
                                </span>

                              </div>

                              <button
                                type="button"
                                className="complaint-view-details"
                                onClick={(event) => {
                                  event.stopPropagation();

                                  navigate(
                                    `/complaints/${encodeURIComponent(
                                      complaint.complaintNumber,
                                    )}`,
                                  );
                                }}
                              >
                                View Details
                              </button>

                            </div>

                            {/* Timeline */}

                            <div className="complaint-timeline">

                              {steps.map(
                                (
                                  step,
                                  stepIndex,
                                ) => (
                                  <div
                                    key={
                                      step.label
                                    }
                                    className={`complaint-timeline-step ${
                                      step.active
                                        ? "is-active"
                                        : ""
                                    }`}
                                  >

                                    <div className="complaint-timeline-node-row">

                                      <span className="complaint-timeline-node">
                                        {step.active ? (
                                          <CheckCircle2
                                            size={17}
                                            strokeWidth={2.5}
                                          />
                                        ) : (
                                          <span />
                                        )}
                                      </span>

                                      {stepIndex <
                                        steps.length -
                                          1 && (
                                        <span
                                          className={`complaint-timeline-line ${
                                            steps[
                                              stepIndex +
                                                1
                                            ].active
                                              ? "is-active"
                                              : ""
                                          }`}
                                        />
                                      )}

                                    </div>

                                    <strong>
                                      {step.label}
                                    </strong>

                                    <small>
                                      {timelineDateFor(
                                        stepIndex,
                                      )}
                                    </small>

                                  </div>
                                ),
                              )}

                            </div>

                            {/* Assigned Officer */}

                            <div className="complaint-assigned-officer-card">

                              {complaint.assignedOfficer ? (
                                <>
                                  <div className="complaint-officer-photo-wrap">

                                    {complaint
                                      .assignedOfficer
                                      .photoUrl ? (
                                      <img
                                        src={
                                          complaint
                                            .assignedOfficer
                                            .photoUrl
                                        }
                                        alt={
                                          complaint
                                            .assignedOfficer
                                            .officerName
                                        }
                                        className="complaint-timeline-officer-photo"
                                      />
                                    ) : (
                                      <span className="complaint-timeline-officer-avatar">
                                        {complaint
                                          .assignedOfficer
                                          .officerName
                                          .split(" ")
                                          .filter(Boolean)
                                          .slice(
                                            0,
                                            2,
                                          )
                                          .map(
                                            (name) =>
                                              name[0]?.toUpperCase(),
                                          )
                                          .join("")}
                                      </span>
                                    )}

                                  </div>

                                  <div className="complaint-timeline-officer-info">

                                    <strong>
                                      {
                                        complaint
                                          .assignedOfficer
                                          .officerName
                                      }
                                    </strong>

                                    {complaint
                                      .assignedOfficer
                                      .designationName && (
                                      <span>
                                        {
                                          complaint
                                            .assignedOfficer
                                            .designationName
                                        }
                                      </span>
                                    )}

                                    {complaint
                                      .assignedOfficer
                                      .departmentName && (
                                      <span>
                                        {
                                          complaint
                                            .assignedOfficer
                                            .departmentName
                                        }
                                      </span>
                                    )}

                                    <span className="complaint-current-status">
                                      Current Status: {complaint.status}
                                    </span>

                                    {complaint
                                      .assignedOfficer
                                      .officeName && (
                                      <span className="complaint-timeline-office">
                                        <MapPin
                                          size={12}
                                        />
                                        {
                                          complaint
                                            .assignedOfficer
                                            .officeName
                                        }
                                      </span>
                                    )}

                                  </div>
                                </>
                              ) : (
                                <div className="complaint-officer-not-assigned">

                                  <UserRound
                                    size={30}
                                  />

                                  <div>
                                    <strong>
                                      Officer not assigned
                                    </strong>

                                    <span>
                                      Assignment is
                                      pending
                                    </span>
                                  </div>

                                </div>
                              )}

                            </div>

                          </article>
                        );
                      },
                    )}

                  </div>
                )}

            </section>

            {/* =====================================
                DEPARTMENTAL / AREA OFFICERS
            ====================================== */}

            <section className="citizen-card officers-directory-card">

              <div className="officers-directory-header">

                <div>
                  <h2>
                    <Users size={21} />
                    Departmental / Area Officers
                  </h2>

                  <p>
                    Apne kshetra ke vibhinn vibhagon ke
                    adhikariyon ki jankari prapt karein.
                  </p>
                </div>

                <button
                  type="button"
                  className="officers-view-all"
                >
                  View All Officers
                  <ChevronRight size={16} />
                </button>

              </div>

              <div className="officers-filters">

                <label>
                  <span>District</span>

                  <select
                    value={selectedDistrictId}
                    onChange={(event) => {
                      const value = event.target.value;

                      setSelectedDistrictId(
                        value === "" ? "" : Number(value),
                      );

                      setSelectedTehsilId("");
                      setSelectedBlockId("");

                      setSelectedMunicipalBodyId("");
                      setSelectedWardId("");
                      setSelectedLocalityId("");
                    }}
                  >
                    <option value="">
                      Select District
                    </option>

                    {districts.map((district) => (
                      <option
                        key={district.id}
                        value={district.id}
                      >
                        {district.district_name}
                      </option>
                    ))}
                  </select>
                </label>

                <label>
                  <span>Area Type</span>

                  <select
                    value={selectedAreaType}
                    disabled={selectedDistrictId === ""}
                    onChange={(event) => {
                      const value =
                        event.target.value as
                          | "rural"
                          | "urban";

                      setSelectedAreaType(value);

                      setSelectedTehsilId("");
                      setSelectedBlockId("");

                      setSelectedMunicipalBodyId("");
                      setSelectedWardId("");
                      setSelectedLocalityId("");
                    }}
                  >
                    <option value="rural">
                      Rural
                    </option>

                    <option value="urban">
                      Urban
                    </option>
                  </select>
                </label>

                {selectedAreaType === "rural" ? (
                  <>
                    <label>
                      <span>Tehsil</span>

                      <select
                        value={selectedTehsilId}
                        disabled={
                          selectedDistrictId === ""
                        }
                        onChange={(event) => {
                          const value =
                            event.target.value;

                          setSelectedTehsilId(
                            value === ""
                              ? ""
                              : Number(value),
                          );

                          setSelectedBlockId("");
                        }}
                      >
                        <option value="">
                          All Tehsils
                        </option>

                        {filteredTehsils.map(
                          (tehsil) => (
                            <option
                              key={tehsil.id}
                              value={tehsil.id}
                            >
                              {tehsil.tehsil_name}
                            </option>
                          ),
                        )}
                      </select>
                    </label>

                    <label>
                      <span>Block / Area</span>

                      <select
                        value={selectedBlockId}
                        disabled={
                          selectedTehsilId === ""
                        }
                        onChange={(event) => {
                          const value =
                            event.target.value;

                          setSelectedBlockId(
                            value === ""
                              ? ""
                              : Number(value),
                          );
                        }}
                      >
                        <option value="">
                          All Areas
                        </option>

                        {filteredBlocks.map(
                          (block) => (
                            <option
                              key={block.id}
                              value={block.id}
                            >
                              {block.block_name}
                            </option>
                          ),
                        )}
                      </select>
                    </label>
                  </>
                ) : (
                  <>
                    <label>
                      <span>Municipal Body</span>

                      <select
                        value={selectedMunicipalBodyId}
                        disabled={
                          selectedDistrictId === ""
                        }
                        onChange={(event) => {
                          const value =
                            event.target.value;

                          setSelectedMunicipalBodyId(
                            value === ""
                              ? ""
                              : Number(value),
                          );

                          setSelectedWardId("");
                          setSelectedLocalityId("");
                        }}
                      >
                        <option value="">
                          All Municipal Bodies
                        </option>

                        {filteredMunicipalBodies.map(
                          (body) => (
                            <option
                              key={body.id}
                              value={body.id}
                            >
                              {body.body_name}
                            </option>
                          ),
                        )}
                      </select>
                    </label>

                    <label>
                      <span>Ward</span>

                      <select
                        value={selectedWardId}
                        disabled={
                          selectedMunicipalBodyId === ""
                        }
                        onChange={(event) => {
                          const value =
                            event.target.value;

                          setSelectedWardId(
                            value === ""
                              ? ""
                              : Number(value),
                          );

                          setSelectedLocalityId("");
                        }}
                      >
                        <option value="">
                          All Wards
                        </option>

                        {filteredWards.map(
                          (ward) => (
                            <option
                              key={ward.id}
                              value={ward.id}
                            >
                              {ward.ward_name}
                            </option>
                          ),
                        )}
                      </select>
                    </label>

                    <label>
                      <span>Locality</span>

                      <select
                        value={selectedLocalityId}
                        disabled={
                          selectedWardId === ""
                        }
                        onChange={(event) => {
                          const value =
                            event.target.value;

                          setSelectedLocalityId(
                            value === ""
                              ? ""
                              : Number(value),
                          );
                        }}
                      >
                        <option value="">
                          All Localities
                        </option>

                        {filteredLocalities.map(
                          (locality) => (
                            <option
                              key={locality.id}
                              value={locality.id}
                            >
                              {locality.locality_name}
                            </option>
                          ),
                        )}
                      </select>
                    </label>
                  </>
                )}

                <label>
                  <span>Department</span>

                  <select
                    value={selectedDepartmentId}
                    onChange={(event) => {
                      const value =
                        event.target.value;

                      setSelectedDepartmentId(
                        value === ""
                          ? ""
                          : Number(value),
                      );
                    }}
                  >
                    <option value="">
                      All Departments
                    </option>

                    {governmentDepartments.map(
                      (department) => (
                        <option
                          key={department.id}
                          value={department.id}
                        >
                          {department.department_name}
                        </option>
                      ),
                    )}
                  </select>
                </label>

              </div>

              <div className="officers-directory-content">

                {officersLoading ? (
                  <div className="officers-directory-empty">
                    <LoaderCircle
                      size={25}
                      className="animate-spin"
                    />

                    <span>
                      Officers loading...
                    </span>
                  </div>
                ) : filteredOfficers.length === 0 ? (
                  <div className="officers-directory-empty">
                    <Users size={28} />

                    <strong>
                      No officers found
                    </strong>

                    <span>
                      Department select karke officers dekhein.
                    </span>
                  </div>
                ) : (
                  <div className="officers-card-grid">

                    {filteredOfficers.map((officer) => {

                      const designation =
                        designations.find(
                          (item) =>
                            item.id ===
                            officer.designation_id,
                        );

                      const office =
                        offices.find(
                          (item) =>
                            item.id ===
                            officer.office_id,
                        );

                      const department =
                        governmentDepartments.find(
                          (item) =>
                            item.id ===
                            officer.department_id,
                        );

                      return (
                        <article
                          className="officer-directory-card"
                          key={officer.id}
                        >

                          <div className="officer-card-main">

                            <div className="officer-avatar">
                              <UserRound size={25} />
                            </div>

                            <div className="officer-card-info">

                              <h3>
                                {officer.officer_name}
                              </h3>

                              <strong>
                                {designation?.designation_name ??
                                  "Designation"}
                              </strong>

                              <span>
                                {department?.department_name ??
                                  "Department"}
                              </span>

                            </div>

                          </div>

                          <div className="officer-card-location">

                            <MapPin size={14} />

                            <span>
                              {office?.office_name ??
                                "Office information unavailable"}
                            </span>

                          </div>

                          <div className="officer-card-actions">

                            <button
                              type="button"
                              onClick={() =>
                                navigate(
                                  `/citizen/officers/${officer.id}`,
                                )
                              }
                            >
                              View Profile
                              <ChevronRight size={15} />
                            </button>

                            <button
                              type="button"
                              className="officer-history-button"
                            >
                              Service History
                            </button>

                          </div>

                        </article>
                      );
                    })}

                  </div>
                )}

              </div>

            </section>

          </div>

          {/* =====================================
              RIGHT COLUMN
          ====================================== */}

          <aside className="citizen-right-column">

            {/* Notifications */}

            <section className="citizen-card notification-card">

              <div className="citizen-section-heading">

                <h2>
                  <Bell size={20} />
                  Important Notifications
                </h2>

                <button
                  type="button"
                  onClick={() =>
                    setShowNotifications(true)
                  }
                >
                  View All
                </button>

              </div>

              <div className="notification-list">

                {notifications.length === 0 ? (
                  <div className="notification-item">

                    <span className="notification-icon blue">
                      <Bell size={19} />
                    </span>

                    <div>
                      <strong>
                        No notifications
                      </strong>
                    </div>

                  </div>
                ) : (
                  notifications.map(
                    (notification) => (
                      <div
                        className="notification-item"
                        key={notification.id}
                      >

                        <span
                          className={`notification-icon ${notification.tone}`}
                        >
                          {notification.tone ===
                          "green" ? (
                            <CheckCircle2
                              size={19}
                            />
                          ) : (
                            <FileText
                              size={19}
                            />
                          )}
                        </span>

                        <div>

                          <strong>
                            {
                              notification.title
                            }
                          </strong>

                          <small>
                            {notification.time}
                          </small>

                        </div>

                        {notification.unread && (
                          <span className="notification-unread" />
                        )}

                      </div>
                    ),
                  )
                )}

              </div>

            </section>

            {/* AI */}

            <section className="citizen-card ai-card">

              <div className="ai-card-heading">

                <h2>
                  <Bot size={21} />
                  AI Assistant
                </h2>

                <Zap size={21} />

              </div>

              <div className="ai-message">
                Namaste! मैं आपका AI सहायक हूँ।
                <br />
                आप मुझसे अपनी शिकायत, सरकारी
                सेवाओं या योजनाओं के बारे में पूछ
                सकते हैं।
              </div>

              <div className="ai-input-row">

                <input
                  type="text"
                  placeholder="Apna prashn yahan likhen..."
                  onKeyDown={(event) => {
                    if (event.key === "Enter") {
                      onOpenAI?.();
                    }
                  }}
                />

                <button
                  type="button"
                  aria-label="Ask AI"
                  onClick={onOpenAI}
                >
                  <ChevronRight size={22} />
                </button>

              </div>

              <div className="ai-suggestions">

                <button
                  type="button"
                  onClick={onOpenAI}
                >
                  मेरी शिकायत का क्या हुआ?
                </button>

                <button
                  type="button"
                  onClick={onOpenAI}
                >
                  जाति प्रमाण पत्र कैसे बनवाएं?
                </button>

              </div>

            </section>

            {/* Voice AI */}

            <section className="citizen-card voice-card">

              <div className="voice-heading">

                <h2>
                  <Mic size={21} />
                  Voice Assistant
                </h2>

                <span>
                  बोलकर अपनी शिकायत दर्ज करें
                </span>

              </div>

              <div
                className="voice-visualizer"
                aria-hidden="true"
              >

                <span />
                <span />
                <span />
                <span />

                <button
                  type="button"
                  aria-label="Start voice assistant"
                  onClick={onOpenVoiceAI}
                >
                  <Mic size={28} />
                </button>

                <span />
                <span />
                <span />
                <span />

              </div>

              <p>
                बोलना शुरू करने के लिए
                माइक्रोफोन पर क्लिक करें
              </p>

            </section>

          </aside>

        </section>

      </main>
  );
}

export default CitizenDashboard;
