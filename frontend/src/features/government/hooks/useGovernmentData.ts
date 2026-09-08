import { useQuery } from "@tanstack/react-query";

import {
  getBlocks,
  getDesignations,
  getLocalities,
  getMunicipalBodies,
  getWards,
  getDistricts,
  getGovernmentDepartments,
  getOfficers,
  getOffices,
  getTehsils,
  getGramPanchayatsByBlock,
  getVillagesByGramPanchayat,
} from "../api/government.api";

export const governmentKeys = {
  all: ["government"] as const,

  districts: () =>
    [...governmentKeys.all, "districts"] as const,

  tehsils: () =>
    [...governmentKeys.all, "tehsils"] as const,

  blocks: () =>
    [...governmentKeys.all, "blocks"] as const,

  gramPanchayatsByBlock: (blockId: number) =>
    [
      ...governmentKeys.all,
      "gram-panchayats",
      "block",
      blockId,
    ] as const,

  villagesByGramPanchayat: (
    gramPanchayatId: number,
  ) =>
    [
      ...governmentKeys.all,
      "villages",
      "gram-panchayat",
      gramPanchayatId,
    ] as const,

  municipalBodies: () =>
    [...governmentKeys.all, "municipal-bodies"] as const,

  wards: () =>
    [...governmentKeys.all, "wards"] as const,

  localities: () =>
    [...governmentKeys.all, "localities"] as const,

  departments: () =>
    [...governmentKeys.all, "departments"] as const,

  designations: () =>
    [...governmentKeys.all, "designations"] as const,

  offices: () =>
    [...governmentKeys.all, "offices"] as const,

  officers: () =>
    [...governmentKeys.all, "officers"] as const,
};

export function useDistricts() {
  return useQuery({
    queryKey: governmentKeys.districts(),
    queryFn: getDistricts,
  });
}

export function useTehsils() {
  return useQuery({
    queryKey: governmentKeys.tehsils(),
    queryFn: getTehsils,
  });
}

export function useBlocks() {
  return useQuery({
    queryKey: governmentKeys.blocks(),
    queryFn: getBlocks,
  });
}

export function useGramPanchayatsByBlock(
  blockId: number | "",
) {
  return useQuery({
    queryKey:
      blockId === ""
        ? [
            ...governmentKeys.all,
            "gram-panchayats",
            "block",
            "disabled",
          ] as const
        : governmentKeys.gramPanchayatsByBlock(
            blockId,
          ),
    queryFn: () =>
      getGramPanchayatsByBlock(
        blockId as number,
      ),
    enabled: blockId !== "",
  });
}

export function useVillagesByGramPanchayat(
  gramPanchayatId: number | "",
) {
  return useQuery({
    queryKey:
      gramPanchayatId === ""
        ? [
            ...governmentKeys.all,
            "villages",
            "gram-panchayat",
            "disabled",
          ] as const
        : governmentKeys.villagesByGramPanchayat(
            gramPanchayatId,
          ),
    queryFn: () =>
      getVillagesByGramPanchayat(
        gramPanchayatId as number,
      ),
    enabled: gramPanchayatId !== "",
  });
}

export function useMunicipalBodies() {
  return useQuery({
    queryKey: governmentKeys.municipalBodies(),
    queryFn: getMunicipalBodies,
  });
}

export function useWards() {
  return useQuery({
    queryKey: governmentKeys.wards(),
    queryFn: getWards,
  });
}

export function useLocalities() {
  return useQuery({
    queryKey: governmentKeys.localities(),
    queryFn: getLocalities,
  });
}

export function useGovernmentDepartments() {
  return useQuery({
    queryKey: governmentKeys.departments(),
    queryFn: getGovernmentDepartments,
  });
}

export function useDesignations() {
  return useQuery({
    queryKey: governmentKeys.designations(),
    queryFn: getDesignations,
  });
}

export function useOffices() {
  return useQuery({
    queryKey: governmentKeys.offices(),
    queryFn: getOffices,
  });
}

export function useGovernmentOfficers() {
  return useQuery({
    queryKey: governmentKeys.officers(),
    queryFn: getOfficers,
  });
}
