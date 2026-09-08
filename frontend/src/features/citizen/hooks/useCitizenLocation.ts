import { useQuery } from "@tanstack/react-query";

import {
  getDistricts,
  getStates,
} from "../api/location.api";

export function useCitizenStates() {
  return useQuery({
    queryKey: ["citizen", "states"],
    queryFn: getStates,
  });
}

export function useCitizenDistricts() {
  return useQuery({
    queryKey: ["citizen", "districts"],
    queryFn: getDistricts,
  });
}
