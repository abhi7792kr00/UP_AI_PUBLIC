import {
  BarChart3,
  Bot,
  Building2,
  FileText,
  LayoutDashboard,
  Map,
  MessageSquare,
  Settings,
  Shield,
  Users,
} from "lucide-react";

import { ROLES, type Role } from "./roles";

export interface NavigationItem {
  label: string;
  path: string;
  icon: typeof LayoutDashboard;
}

export const PUBLIC_NAVIGATION: NavigationItem[] = [
  {
    label: "Home",
    path: "/",
    icon: LayoutDashboard,
  },
  {
    label: "Track Complaint",
    path: "/track",
    icon: FileText,
  },
  {
    label: "Officers",
    path: "/officers",
    icon: Users,
  },
  {
    label: "Departments",
    path: "/departments",
    icon: Building2,
  },
  {
    label: "AI Assistant",
    path: "/ai",
    icon: Bot,
  },
];

export const ROLE_NAVIGATION: Record<Role, NavigationItem[]> = {
  [ROLES.CITIZEN]: [
    {
      label: "Dashboard",
      path: "/citizen",
      icon: LayoutDashboard,
    },
    {
      label: "My Complaints",
      path: "/citizen/complaints",
      icon: FileText,
    },
    {
      label: "Register Complaint",
      path: "/citizen/complaints/new",
      icon: MessageSquare,
    },
    {
      label: "Officer Directory",
      path: "/citizen/officers",
      icon: Users,
    },
    {
      label: "AI Assistant",
      path: "/citizen/ai",
      icon: Bot,
    },
  ],

  [ROLES.OFFICER]: [
    {
      label: "Dashboard",
      path: "/officer",
      icon: LayoutDashboard,
    },
    {
      label: "My Complaints",
      path: "/officer/complaints",
      icon: FileText,
    },
    {
      label: "Department",
      path: "/officer/department",
      icon: Building2,
    },
    {
      label: "Officers",
      path: "/officer/officers",
      icon: Users,
    },
    {
      label: "SLA & Performance",
      path: "/officer/performance",
      icon: BarChart3,
    },
  ],

  [ROLES.DISTRICT_DM]: [
    {
      label: "District Overview",
      path: "/dm",
      icon: LayoutDashboard,
    },
    {
      label: "Complaints",
      path: "/dm/complaints",
      icon: FileText,
    },
    {
      label: "Departments",
      path: "/dm/departments",
      icon: Building2,
    },
    {
      label: "Officers",
      path: "/dm/officers",
      icon: Users,
    },
    {
      label: "District Analytics",
      path: "/dm/analytics",
      icon: BarChart3,
    },
    {
      label: "Escalations",
      path: "/dm/escalations",
      icon: Shield,
    },
  ],

  [ROLES.DISTRICT_SP]: [
    {
      label: "Police Overview",
      path: "/sp",
      icon: LayoutDashboard,
    },
    {
      label: "Police Complaints",
      path: "/sp/complaints",
      icon: FileText,
    },
    {
      label: "Police Officers",
      path: "/sp/officers",
      icon: Users,
    },
    {
      label: "Performance",
      path: "/sp/performance",
      icon: BarChart3,
    },
    {
      label: "District Map",
      path: "/sp/map",
      icon: Map,
    },
  ],

  [ROLES.DISTRICT_CDO]: [
    {
      label: "Development Overview",
      path: "/cdo",
      icon: LayoutDashboard,
    },
    {
      label: "Complaints",
      path: "/cdo/complaints",
      icon: FileText,
    },
    {
      label: "Officers",
      path: "/cdo/officers",
      icon: Users,
    },
    {
      label: "Development Analytics",
      path: "/cdo/analytics",
      icon: BarChart3,
    },
  ],

  [ROLES.DISTRICT_CMO]: [
    {
      label: "Health Overview",
      path: "/cmo",
      icon: LayoutDashboard,
    },
    {
      label: "Health Complaints",
      path: "/cmo/complaints",
      icon: FileText,
    },
    {
      label: "Health Officers",
      path: "/cmo/officers",
      icon: Users,
    },
    {
      label: "Health Analytics",
      path: "/cmo/analytics",
      icon: BarChart3,
    },
  ],

  [ROLES.DISTRICT_ADMIN]: [
    {
      label: "District Dashboard",
      path: "/district-admin",
      icon: LayoutDashboard,
    },
    {
      label: "Departments",
      path: "/district-admin/departments",
      icon: Building2,
    },
    {
      label: "Officers",
      path: "/district-admin/officers",
      icon: Users,
    },
    {
      label: "Complaints",
      path: "/district-admin/complaints",
      icon: FileText,
    },
    {
      label: "Reports",
      path: "/district-admin/reports",
      icon: BarChart3,
    },
    {
      label: "Audit Logs",
      path: "/district-admin/audit",
      icon: Shield,
    },
  ],

  [ROLES.SUPER_ADMIN]: [
    {
      label: "State Overview",
      path: "/super-admin",
      icon: LayoutDashboard,
    },
    {
      label: "Districts",
      path: "/super-admin/districts",
      icon: Map,
    },
    {
      label: "Departments",
      path: "/super-admin/departments",
      icon: Building2,
    },
    {
      label: "Officers",
      path: "/super-admin/officers",
      icon: Users,
    },
    {
      label: "Complaints",
      path: "/super-admin/complaints",
      icon: FileText,
    },
    {
      label: "Analytics",
      path: "/super-admin/analytics",
      icon: BarChart3,
    },
    {
      label: "Roles & Permissions",
      path: "/super-admin/roles",
      icon: Settings,
    },
    {
      label: "Audit Logs",
      path: "/super-admin/audit",
      icon: Shield,
    },
  ],
};