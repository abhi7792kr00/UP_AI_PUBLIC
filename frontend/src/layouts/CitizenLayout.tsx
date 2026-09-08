import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import {
  Bell,
  ChevronDown,
  Globe2,
  Home,
  LogOut,
  Menu,
  FileText,
  ShieldCheck,
  UserRound,
  X,
  Settings,
  Sparkles,
  Mic,
  UserCircle,
} from "lucide-react";

import { useAuthStore } from "../stores/auth.store";
import { useLogout } from "../features/auth/hooks/useLogout";

import { initializeCitizenTheme } from "../theme/citizenTheme";

import "../pages/citizen/citizen-dashboard.css";
import { getCitizenTranslations } from "../i18n/citizenTranslations";

export function CitizenLayout() {
    useEffect(() => {
    initializeCitizenTheme();
    }, []);

  const navigate = useNavigate();
  const location = useLocation();
  const logout = useLogout();

  const user = useAuthStore((state) => state.user);

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [language, setLanguageState] = useState<"Hindi" | "English">(
    () =>
      (localStorage.getItem("upai_language") as "Hindi" | "English") ||
      "Hindi",
  );

  const setLanguage = (value: "Hindi" | "English") => {
    setLanguageState(value);
    localStorage.setItem("upai_language", value);
    window.dispatchEvent(new Event("upai-language-change"));
  };

  const t = getCitizenTranslations(language);

  const closeSidebar = () => {
    setSidebarOpen(false);
  };

  const handleLogout = () => {
    logout();
    navigate("/login/citizen", { replace: true });
  };

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  const navItems = [
    {
      label: t.dashboard,
      path: "/citizen",
      icon: Home,
    },
    {
      label: t.myComplaints,
      path: "/citizen/complaints",
      icon: FileText,
    },
    {
      label: t.documents,
      path: "/citizen/documents",
      icon: FileText,
    },
    {
      label: t.notifications,
      path: "/citizen/notifications",
      icon: Bell,
    },
    {
      label: t.aiAssistant,
      path: "/ai",
      icon: Sparkles,
    },
    {
      label: t.voiceAI,
      path: "/citizen/voice",
      icon: Mic,
    },
    {
      label: t.profile,
      path: "/citizen/profile",
      icon: UserCircle,
    },
    {
      label: t.settings,
      path: "/citizen/settings",
      icon: Settings,
    },
  ];

  return (
    <div
      className={`citizen-dashboard ${
        language === "Hindi"
          ? "citizen-language-hindi"
          : "citizen-language-english"
      }`}
    >
      {/* =====================================================
          TOP BAR
      ====================================================== */}
      <header className="citizen-topbar">
        <div className="citizen-brand">
          <div
            className="citizen-emblem"
            aria-label="Uttar Pradesh Government"
          >
            <ShieldCheck
              size={28}
              strokeWidth={2.2}
            />
          </div>

          <div className="citizen-brand-copy">
            <div>
              <strong>UP_AI</strong>

              <span className="brand-divider">|</span>

              <span className="portal-name">
                {t.citizenPortal}
              </span>
            </div>

            <small>
              जन सामान्य की सेवा में, सदैव साथ
            </small>
          </div>
        </div>

        <div className="citizen-topbar-actions">
          <button
            className="citizen-icon-button"
            type="button"
            aria-label="Notifications"
          >
            <Bell size={20} />
          </button>

          <button
            className="citizen-language-button"
            type="button"
            onClick={() =>
              setLanguage(
                language === "Hindi"
                  ? "English"
                  : "Hindi",
              )
            }
          >
            <Globe2 size={17} />
            <span>{language}</span>
            <ChevronDown size={15} />
          </button>

          <button
            className="citizen-user-menu"
            type="button"
          >
            <span className="citizen-avatar">
              <UserRound size={21} />
            </span>

            <span className="citizen-user-copy">
              <strong>
                {user?.full_name ?? "Citizen"}
              </strong>

              <small>Citizen</small>
            </span>

            <ChevronDown size={16} />
          </button>

          <button
            className="citizen-mobile-menu"
            type="button"
            aria-label="Open menu"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu size={22} />
          </button>
        </div>
      </header>

      {/* =====================================================
          SIDEBAR
      ====================================================== */}
      <aside
        className={`citizen-sidebar ${
          sidebarOpen ? "is-open" : ""
        }`}
      >
        <div className="citizen-sidebar-inner">
          <div className="citizen-sidebar-mobile-head">
            <div className="citizen-mobile-brand">
              <ShieldCheck size={21} />
              <strong>UP_AI</strong>
            </div>

            <button
              type="button"
              onClick={closeSidebar}
              aria-label="Close menu"
            >
              <X size={21} />
            </button>
          </div>

          <div className="citizen-sidebar-section-title">
            <span>PORTAL</span>
          </div>

          <nav
            className="citizen-sidebar-nav"
            aria-label="Citizen navigation"
          >
            {navItems.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.path);

              return (
                <button
                  key={item.label}
                  className={`citizen-nav-item ${
                    active ? "active" : ""
                  }`}
                  type="button"
                  title={item.label}
                  onClick={() => {
                    closeSidebar();
                    navigate(item.path);
                  }}
                >
                  <span className="citizen-nav-icon">
                    <Icon size={19} strokeWidth={2} />
                  </span>

                  <span className="citizen-nav-label">
                    {item.label}
                  </span>
                </button>
              );
            })}
          </nav>

          <div className="citizen-sidebar-footer">
            <button
              className="citizen-nav-item citizen-logout"
              type="button"
              onClick={handleLogout}
              title="Logout"
            >
              <span className="citizen-nav-icon">
                <LogOut size={19} />
              </span>

              <span className="citizen-nav-label">
                Logout
              </span>
            </button>
          </div>
        </div>
      </aside>

      {/* MOBILE OVERLAY */}
      {sidebarOpen && (
        <button
          className="citizen-sidebar-overlay"
          type="button"
          aria-label="Close menu"
          onClick={closeSidebar}
        />
      )}

      {/* =====================================================
          PAGE CONTENT
      ====================================================== */}
      <main className="citizen-content">
        <Outlet />
      </main>
    </div>
  );
}

export default CitizenLayout;
