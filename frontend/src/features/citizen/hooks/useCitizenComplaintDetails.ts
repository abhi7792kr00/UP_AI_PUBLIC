import { useQuery } from "@tanstack/react-query";
import {
  getMyComplaint,
  getComplaintTimeline,
} from "../api/citizen.api";
import { useAuthStore } from "../../../stores/auth.store";

export const citizenComplaintDetailKeys = {
  all: ["citizen", "complaint-detail"] as const,
  detail: (complaintNumber: string, userId?: number | null) =>
    [
      ...citizenComplaintDetailKeys.all,
      complaintNumber,
      userId ?? "anonymous",
    ] as const,
  timeline: (complaintNumber: string, userId?: number | null) =>
    [
      ...citizenComplaintDetailKeys.detail(complaintNumber, userId),
      "timeline",
    ] as const,
};

export function useMyComplaintDetails(complaintNumber: string) {
  const userId = useAuthStore((s) => s.user?.id);

  return useQuery({
    queryKey: citizenComplaintDetailKeys.detail(complaintNumber, userId),
    queryFn: () => getMyComplaint(complaintNumber),
    enabled: Boolean(complaintNumber) && Boolean(userId),
    retry: false,
  });
}

export function useMyComplaintTimeline(complaintNumber: string) {
  const userId = useAuthStore((s) => s.user?.id);

  return useQuery({
    queryKey: citizenComplaintDetailKeys.timeline(complaintNumber, userId),
    queryFn: () => getComplaintTimeline(complaintNumber),
    enabled: Boolean(complaintNumber) && Boolean(userId),
    retry: false,
  });
}
