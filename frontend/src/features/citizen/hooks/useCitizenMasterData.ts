import { useQuery } from "@tanstack/react-query";

import {
  getComplaintCategories,
  getDepartments,
} from "../api/master-data.api";

export function useCitizenComplaintCategories() {
  return useQuery({
    queryKey: ["citizen", "complaint-categories"],
    queryFn: getComplaintCategories,
  });
}

export function useCitizenDepartments() {
  return useQuery({
    queryKey: ["citizen", "departments"],
    queryFn: getDepartments,
  });
}
