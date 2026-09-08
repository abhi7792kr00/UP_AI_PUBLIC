import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  createMyComplaint,
  getMyComplaint,
  getMyComplaints,
  type CitizenComplaintCreate,
} from "../api/citizen.api";

import { useAuthStore } from "../../../stores/auth.store";

export const citizenComplaintKeys = {
  all: ["citizen", "complaints"] as const,
  list: (userId?: number | null) =>
    [...citizenComplaintKeys.all, "list", userId ?? "anonymous"] as const,
  detail: (complaintNumber: string, userId?: number | null) =>
    [
      ...citizenComplaintKeys.all,
      complaintNumber,
      userId ?? "anonymous",
    ] as const,
};

export function useMyComplaints() {
  const userId = useAuthStore((s) => s.user?.id);

  return useQuery({
    queryKey: citizenComplaintKeys.list(userId),
    queryFn: getMyComplaints,
    enabled: Boolean(userId),
  });
}

export function useMyComplaint(complaintNumber: string) {
  const userId = useAuthStore((s) => s.user?.id);

  return useQuery({
    queryKey: citizenComplaintKeys.detail(complaintNumber, userId),
    queryFn: () => getMyComplaint(complaintNumber),
    enabled: Boolean(complaintNumber) && Boolean(userId),
  });
}

export function useCreateMyComplaint() {
  const queryClient = useQueryClient();
  const userId = useAuthStore((s) => s.user?.id);

  return useMutation({
    mutationFn: (payload: CitizenComplaintCreate) =>
      createMyComplaint(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: citizenComplaintKeys.list(userId),
      });
    },
  });
}
