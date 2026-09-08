import type { CitizenComplaint } from "../api/citizen.api";
import type {
  ComplaintCategory,
  ComplaintStatus,
  Department,
} from "../../complaints/api/master-data.api";

import type { CitizenDashboardComplaint } from "../../../pages/citizen/CitizenDashboard";

import {
  formatBackendDate,
  parseBackendDate,
} from "../../../utils/backend-date";

function getIcon(
  category: ComplaintCategory | undefined,
): CitizenDashboardComplaint["icon"] {
  const value = (
    `${category?.category_code ?? ""} ${category?.category_name ?? ""}`
  ).toLowerCase();

  if (value.includes("electric")) return "electricity";
  if (value.includes("road") || value.includes("pwd")) return "road";
  if (value.includes("water") || value.includes("jal")) return "water";
  if (value.includes("revenue") || value.includes("raj")) return "revenue";
  if (value.includes("health") || value.includes("medical")) return "health";

  return undefined;
}

function mapStatus(
  status: ComplaintStatus | undefined,
): CitizenDashboardComplaint["status"] {
  const value = (
    status?.status_name ??
    status?.status_code ??
    ""
  ).toLowerCase();

  if (
    value.includes("resolved") ||
    value.includes("closed") ||
    value.includes("complete")
  ) {
    return "Resolved";
  }

  if (
    value.includes("progress") ||
    value.includes("assigned") ||
    value.includes("processing")
  ) {
    return "In Progress";
  }

  return "Pending";
}

export function mapCitizenComplaint(
  complaint: CitizenComplaint,
  categories: ComplaintCategory[],
  departments: Department[],
  statuses: ComplaintStatus[],
): CitizenDashboardComplaint {
  const category = categories.find(
    (item) => item.id === complaint.category_id,
  );

  const department = complaint.department_id
    ? departments.find(
        (item) => item.id === complaint.department_id,
      )
    : undefined;

  const status = complaint.status_id
    ? statuses.find(
        (item) => item.id === complaint.status_id,
      )
    : undefined;

  return {
    complaintNumber: complaint.complaint_number,
    subject: complaint.subject,

    category:
      category?.category_name ??
      "Category unavailable",

    department:
      department?.department_name ??
      "Department unavailable",

    status: mapStatus(status),

    date: formatBackendDate(
      complaint.created_at,
    ),

    createdAt: complaint.created_at,

    assignedOfficer: complaint.assigned_officer
      ? {
          id: complaint.assigned_officer.id,
          officerName:
            complaint.assigned_officer.officer_name,
          photoUrl:
            complaint.assigned_officer.photo_url,
          mobile:
            complaint.assigned_officer.mobile,
          email:
            complaint.assigned_officer.email,
          designationName:
            complaint.assigned_officer.designation_name,
          departmentName:
            complaint.assigned_officer.department_name,
          officeName:
            complaint.assigned_officer.office_name,
        }
      : null,

    icon: getIcon(category),
  };
}
