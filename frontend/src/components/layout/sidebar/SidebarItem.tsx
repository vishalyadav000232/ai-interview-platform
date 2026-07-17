import { NavLink } from "react-router-dom";
import type { SidebarItemType } from "./sidebar.type";



type SidebarItemProps = {
    item: SidebarItemType;
};

export function SidebarItem({ item }: SidebarItemProps) {
    const Icon = item.icon;

    return (
        <NavLink
            to={item.path}
            className={({ isActive }) =>
                [
                    "group flex items-center gap-3 rounded-lg px-4 py-3",
                    "text-sm font-medium transition-colors",
                    isActive
                        ? "bg-violet-600/25 text-white"
                        : "text-slate-300 hover:bg-white/5 hover:text-white",
                ].join(" ")
            }
        >
            <Icon
                className="h-5 w-5 shrink-0"
                strokeWidth={1.8}
                aria-hidden="true"
            />

            <span>{item.label}</span>
        </NavLink>
    );
}
