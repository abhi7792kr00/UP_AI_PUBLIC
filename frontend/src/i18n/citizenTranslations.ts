export type CitizenLanguage = "Hindi" | "English";

const translations = {
  English: {
    dashboard: "Dashboard",
    myComplaints: "My Complaints",
    documents: "Documents",
    notifications: "Notifications",
    aiAssistant: "AI Assistant",
    voiceAI: "Voice AI",
    profile: "Profile",
    settings: "Settings",
    logout: "Logout",

    citizenPortal: "Citizen Portal",
    welcome: "Welcome",
    totalComplaints: "Total Complaints",
    pending: "Pending",
    inProgress: "In Progress",
    resolved: "Resolved",

    newComplaint: "New Complaint",
    trackComplaint: "Track Complaint",
    recentComplaints: "Recent Complaints",
    importantNotifications: "Important Notifications",

    askAI: "Ask UP_AI",
    submitComplaint: "Submit Complaint",
    helpSupport: "Help & Support",
  },

  Hindi: {
    dashboard: "डैशबोर्ड",
    myComplaints: "मेरी शिकायतें",
    documents: "दस्तावेज़",
    notifications: "सूचनाएँ",
    aiAssistant: "AI सहायक",
    voiceAI: "वॉइस AI",
    profile: "प्रोफ़ाइल",
    settings: "सेटिंग्स",
    logout: "लॉग आउट",

    citizenPortal: "नागरिक पोर्टल",
    welcome: "स्वागत है",
    totalComplaints: "कुल शिकायतें",
    pending: "लंबित",
    inProgress: "प्रगति पर",
    resolved: "निस्तारित",

    newComplaint: "नई शिकायत",
    trackComplaint: "शिकायत ट्रैक करें",
    recentComplaints: "हाल की शिकायतें",
    importantNotifications: "महत्वपूर्ण सूचनाएँ",

    askAI: "UP_AI से पूछें",
    submitComplaint: "शिकायत दर्ज करें",
    helpSupport: "सहायता एवं समर्थन",
  },
} as const;

export function getCitizenTranslations(
  language: CitizenLanguage,
) {
  return translations[language];
}
