export const ROLES = {
  CITIZEN: "CITIZEN",

  OFFICER: "OFFICER",

  DISTRICT_DM: "DISTRICT_DM",
  DISTRICT_SP: "DISTRICT_SP",
  DISTRICT_CDO: "DISTRICT_CDO",
  DISTRICT_CMO: "DISTRICT_CMO",

  DISTRICT_ADMIN: "DISTRICT_ADMIN",

  SUPER_ADMIN: "SUPER_ADMIN",
} as const;

export type Role = (typeof ROLES)[keyof typeof ROLES];

export const LOGIN_PORTALS = {
  CITIZEN: "/login/citizen",
  OFFICER: "/login/officer",
  DM: "/login/dm",
  SP: "/login/sp",
  CDO: "/login/cdo",
  CMO: "/login/cmo",
  DISTRICT_ADMIN: "/login/district-admin",
  SUPER_ADMIN: "/login/super-admin",
} as const;