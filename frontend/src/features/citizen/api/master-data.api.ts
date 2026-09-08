import { api } from "../../../services/api/client";

export interface ComplaintCategory {
  id: number;
  category_name: string;
  category_code: string;
  description: string | null;
  icon: string | null;
  color: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ComplaintSubcategory {
  id: number;
  category_id: number;
  subcategory_name: string;
  subcategory_code?: string;
  description?: string | null;
  is_active?: boolean;
}

export interface ComplaintPriority {
  id: number;
  priority_name: string;
  priority_code: string;
  level?: number;
  color?: string | null;
  description?: string | null;
}

export interface Department {
  id: number;
  department_name: string;
  department_code: string;
  description: string | null;
  is_active: boolean;
}

/** Fallback priorities when backend has no /priorities endpoint */
export const FALLBACK_PRIORITIES: ComplaintPriority[] = [
  {
    id: 1,
    priority_name: "Low",
    priority_code: "LOW",
    level: 1,
    color: "#22c55e",
  },
  {
    id: 2,
    priority_name: "Medium",
    priority_code: "MEDIUM",
    level: 2,
    color: "#eab308",
  },
  {
    id: 3,
    priority_name: "High",
    priority_code: "HIGH",
    level: 3,
    color: "#f97316",
  },
  {
    id: 4,
    priority_name: "Critical",
    priority_code: "CRITICAL",
    level: 4,
    color: "#ef4444",
  },
];

/**
 * Fallback subcategories mapped by common category names.
 * Used when backend does not expose /complaint-subcategories.
 * Keys are lower-cased category names for matching.
 */
export const FALLBACK_SUBCATEGORIES: Record<
  string,
  Array<{ id: number; subcategory_name: string }>
> = {
  electricity: [
    { id: 101, subcategory_name: "Power Outage" },
    { id: 102, subcategory_name: "Voltage Fluctuation" },
    { id: 103, subcategory_name: "Street Light Issue" },
    { id: 104, subcategory_name: "Meter / Billing Issue" },
  ],
  "water supply": [
    { id: 201, subcategory_name: "No Water Supply" },
    { id: 202, subcategory_name: "Contaminated Water" },
    { id: 203, subcategory_name: "Pipeline Leakage" },
    { id: 204, subcategory_name: "Handpump Not Working" },
  ],
  "road & drainage": [
    { id: 301, subcategory_name: "Road Damage / Potholes" },
    { id: 302, subcategory_name: "Drainage Blockage" },
    { id: 303, subcategory_name: "Flooding" },
    { id: 304, subcategory_name: "New Road Request" },
  ],
  revenue: [
    { id: 401, subcategory_name: "Land Record Correction" },
    { id: 402, subcategory_name: "Mutation Delay" },
    { id: 403, subcategory_name: "Certificate Issue" },
    { id: 404, subcategory_name: "Other Revenue Matter" },
  ],
  health: [
    { id: 501, subcategory_name: "Hospital / PHC Issue" },
    { id: 502, subcategory_name: "Medicine Shortage" },
    { id: 503, subcategory_name: "Ambulance Delay" },
    { id: 504, subcategory_name: "Sanitation / Hygiene" },
  ],
  education: [
    { id: 601, subcategory_name: "School Infrastructure" },
    { id: 602, subcategory_name: "Teacher Shortage" },
    { id: 603, subcategory_name: "Scholarship Issue" },
    { id: 604, subcategory_name: "Mid-day Meal" },
  ],
  police: [
    { id: 701, subcategory_name: "Law & Order" },
    { id: 702, subcategory_name: "Traffic Issue" },
    { id: 703, subcategory_name: "FIR Related" },
    { id: 704, subcategory_name: "Other Police Matter" },
  ],
  municipal: [
    { id: 801, subcategory_name: "Garbage Collection" },
    { id: 802, subcategory_name: "Street Cleaning" },
    { id: 803, subcategory_name: "Building Permission" },
    { id: 804, subcategory_name: "Other Municipal Issue" },
  ],
  default: [
    { id: 901, subcategory_name: "General Issue" },
    { id: 902, subcategory_name: "Service Delay" },
    { id: 903, subcategory_name: "Infrastructure Problem" },
    { id: 904, subcategory_name: "Other" },
  ],
};

export async function getComplaintCategories() {
  const response = await api.get<ComplaintCategory[]>(
    "/complaint-categories/",
  );
  return response.data;
}

export async function getDepartments() {
  const response = await api.get<Department[]>("/departments/");
  return response.data;
}

/**
 * Try backend subcategories first; fall back to static list filtered by category.
 */
export async function getComplaintSubcategories(
  categoryId?: number,
): Promise<ComplaintSubcategory[]> {
  try {
    const url =
      categoryId != null && categoryId > 0
        ? `/complaint-subcategories/?category_id=${categoryId}`
        : "/complaint-subcategories/";
    const response = await api.get<ComplaintSubcategory[]>(url);
    if (Array.isArray(response.data) && response.data.length > 0) {
      return response.data;
    }
  } catch {
    // Backend may not have this endpoint yet
  }
  return [];
}

/**
 * Try backend priorities; fall back to static list.
 */
export async function getComplaintPriorities(): Promise<
  ComplaintPriority[]
> {
  try {
    const response = await api.get<ComplaintPriority[]>("/priorities/");
    if (Array.isArray(response.data) && response.data.length > 0) {
      return response.data;
    }
  } catch {
    // Backend may not have this endpoint yet
  }
  return FALLBACK_PRIORITIES;
}

/**
 * Build fallback subcategories for a given category name.
 */
export function getFallbackSubcategoriesForCategory(
  categoryName: string,
  categoryId: number,
): ComplaintSubcategory[] {
  const key = categoryName.trim().toLowerCase();
  const matched =
    FALLBACK_SUBCATEGORIES[key] ??
    Object.entries(FALLBACK_SUBCATEGORIES).find(([k]) =>
      key.includes(k) || k.includes(key),
    )?.[1] ??
    FALLBACK_SUBCATEGORIES.default;

  return matched.map((item) => ({
    id: item.id,
    category_id: categoryId,
    subcategory_name: item.subcategory_name,
    is_active: true,
  }));
}
