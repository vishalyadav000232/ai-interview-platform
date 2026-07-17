
import type { SidebarSectionType } from "./sidebar.type";
import { SidebarItem } from "./SidebarItem";

type SidebarSectionProps = {
  section: SidebarSectionType;
};

export function SidebarSection({
  section,
}: SidebarSectionProps) {
  return (
    <section className="space-y-3">
      {section.title && (
        <p className="px-4 text-xs font-medium uppercase tracking-wider text-slate-500">
          {section.title}
        </p>
      )}

      <nav className="space-y-1">
        {section.items.map((item) => (
          <SidebarItem
            key={item.path}
            item={item}
          />
        ))}
      </nav>
    </section>
  );
}
