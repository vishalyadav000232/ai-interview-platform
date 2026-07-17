import {
    BarChart3,
    CircleHelp,
    Clock3,
    Code2,
    FileText,
    LayoutDashboard,
    Settings,
    UserRound,
    Video,
} from "lucide-react";
import type { SidebarSectionType } from "./sidebar.type";



export const mainSidebarSection: SidebarSectionType = {
    items: [
        {
            label: "Dashboard",
            path: "/dashboard",
            icon: LayoutDashboard,
        },
        {
            label: "Resume",
            path: "/resume",
            icon: FileText,
        },
        {
            label: "Mock Interviews",
            path: "/interviews",
            icon: Video,
        },
        {
            label: "Practice",
            path: "/practice",
            icon: Code2,
        },
        {
            label: "Interview History",
            path: "/history",
            icon: Clock3,
        },
        {
            label: "Progress",
            path: "/progress",
            icon: BarChart3,
        },
    ],
};

export const accountSidebarSection: SidebarSectionType = {
    title: "ACCOUNT",
    items: [
        {
            label: "Profile",
            path: "/profile",
            icon: UserRound,
        },
        {
            label: "Settings",
            path: "/settings",
            icon: Settings,
        },
        {
            label: "Help & Support",
            path: "/support",
            icon: CircleHelp,
        },
    ],
};
