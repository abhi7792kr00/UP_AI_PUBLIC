import { useMutation, useQueryClient } from "@tanstack/react-query";

import {
  createMyComplaint,
  type CitizenComplaintCreate,
} from "../api/citizen.api";

export function useCreateCitizenComplaint() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: CitizenComplaintCreate) =>
      createMyComplaint(payload),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["citizen", "complaints"],
      });
    },
  });
}
