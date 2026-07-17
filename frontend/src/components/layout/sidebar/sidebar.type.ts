import type { LucideIcon } from "lucide-react";

export type SidebarItemType = {
    label: string;
    path: string;
    icon: LucideIcon;
};

export type SidebarSectionType = {
    title?: string;
    items: SidebarItemType[];
};
