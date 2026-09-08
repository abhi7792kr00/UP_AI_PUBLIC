import { useQuery } from "@tanstack/react-query";

import {
  getComplaintCategories,
  getDepartments,
  getComplaintStatuses,
} from "../api/master-data.api";

export const complaintMasterKeys = {
  all: ["complaint-master-data"] as const,

  categories: () => [
    ...complaintMasterKeys.all,
    "categories",
  ] as const,

  departments: () => [
    ...complaintMasterKeys.all,
    "departments",
  ] as const,

  statuses: () => [
    ...complaintMasterKeys.all,
    "statuses",
  ] as const,
};

export function useComplaintCategories() {
  return useQuery({
    queryKey: complaintMasterKeys.categories(),
    queryFn: getComplaintCategories,
  });
}

export function useDepartments() {
  return useQuery({
    queryKey: complaintMasterKeys.departments(),
    queryFn: getDepartments,
  });
}

export function useComplaintStatuses() {
  return useQuery({
    queryKey: complaintMasterKeys.statuses(),
    queryFn: getComplaintStatuses,
  });
}
