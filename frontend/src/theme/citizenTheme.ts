export type CitizenTheme = "light" | "dark" | "system";

const STORAGE_KEY = "upai_citizen_theme";

export function getCitizenTheme(): CitizenTheme {
  const saved = localStorage.getItem(STORAGE_KEY);

  if (
    saved === "light" ||
    saved === "dark" ||
    saved === "system"
  ) {
    return saved;
  }

  return "system";
}

export function getResolvedCitizenTheme(
  theme: CitizenTheme,
): "light" | "dark" {
  if (theme === "light") {
    return "light";
  }

  if (theme === "dark") {
    return "dark";
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

export function applyCitizenTheme(theme: CitizenTheme) {
  const root = document.documentElement;
  const resolvedTheme = getResolvedCitizenTheme(theme);

  root.setAttribute("data-citizen-theme", resolvedTheme);

  localStorage.setItem(STORAGE_KEY, theme);

  window.dispatchEvent(
    new CustomEvent("upai-theme-change", {
      detail: theme,
    }),
  );
}

export function initializeCitizenTheme() {
  const theme = getCitizenTheme();

  applyCitizenTheme(theme);

  if (theme === "system") {
    const mediaQuery = window.matchMedia(
      "(prefers-color-scheme: dark)",
    );

    const handleSystemThemeChange = () => {
      if (getCitizenTheme() === "system") {
        applyCitizenTheme("system");
      }
    };

    mediaQuery.addEventListener(
      "change",
      handleSystemThemeChange,
    );
  }
}
