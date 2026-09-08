import { useQuery } from "@tanstack/react-query";

import {
  getComplaintCategories,
  getComplaintPriorities,
  getComplaintSubcategories,
  getDepartments,
  getFallbackSubcategoriesForCategory,
  type ComplaintSubcategory,
} from "../api/master-data.api";

import {
  getStates,
  getDistricts,
} from "../api/location.api";

export function useCitizenComplaintFormData(selectedCategoryId?: number) {
  const categories = useQuery({
    queryKey: ["citizen", "complaint-categories"],
    queryFn: getComplaintCategories,
  });

  const departments = useQuery({
    queryKey: ["citizen", "departments"],
    queryFn: getDepartments,
  });

  const states = useQuery({
    queryKey: ["citizen", "states"],
    queryFn: getStates,
  });

  const districts = useQuery({
    queryKey: ["citizen", "districts"],
    queryFn: getDistricts,
  });

  const priorities = useQuery({
    queryKey: ["citizen", "complaint-priorities"],
    queryFn: getComplaintPriorities,
  });

  const subcategories = useQuery({
    queryKey: [
      "citizen",
      "complaint-subcategories",
      selectedCategoryId ?? 0,
    ],
    queryFn: async (): Promise<ComplaintSubcategory[]> => {
      if (!selectedCategoryId || selectedCategoryId <= 0) {
        return [];
      }

      const fromApi = await getComplaintSubcategories(selectedCategoryId);
      if (fromApi.length > 0) {
        return fromApi.filter(
          (s) => s.category_id === selectedCategoryId || !s.category_id,
        );
      }

      const category = (categories.data ?? []).find(
        (c) => c.id === selectedCategoryId,
      );
      if (!category) return [];

      return getFallbackSubcategoriesForCategory(
        category.category_name,
        category.id,
      );
    },
    enabled: !!selectedCategoryId && selectedCategoryId > 0,
  });

  return {
    categories: categories.data ?? [],
    departments: departments.data ?? [],
    states: states.data ?? [],
    districts: districts.data ?? [],
    priorities: priorities.data ?? [],
    subcategories: subcategories.data ?? [],

    isLoading:
      categories.isLoading ||
      departments.isLoading ||
      states.isLoading ||
      districts.isLoading ||
      priorities.isLoading,

    isSubcategoriesLoading: subcategories.isLoading,

    isError:
      categories.isError ||
      departments.isError ||
      states.isError ||
      districts.isError,
  };
}
