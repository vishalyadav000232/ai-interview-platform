import {
  ArrowRight,
  Boxes,
  Database,
  Network,
  ServerCog,
  Workflow,
} from "lucide-react";

const missingSkills = [
  {
    name: "Docker",
    icon: Boxes,
    iconClass: "text-sky-400",
  },
  {
    name: "Redis",
    icon: Database,
    iconClass: "text-red-400",
  },
  {
    name: "Kafka",
    icon: Network,
    iconClass: "text-violet-400",
  },
  {
    name: "System Design",
    icon: Workflow,
    iconClass: "text-slate-300",
  },
  {
    name: "SQL Optimization",
    icon: ServerCog,
    iconClass: "text-blue-300",
  },
];

export const MissingSkills = () => {
  return (
    <section className="rounded-xl border border-white/10 bg-[#0b0f17] p-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-[11px] font-semibold text-white">
          Missing Skills
        </h2>

        <button
          type="button"
          className="group inline-flex items-center gap-1 text-[10px] font-medium text-violet-400 transition hover:text-violet-300"
        >
          View All

          <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
        </button>
      </div>

      {/* Skills */}
      <div className="mt-4 flex flex-wrap gap-2">
        {missingSkills.map((skill) => {
          const Icon = skill.icon;

          return (
            <button
              key={skill.name}
              type="button"
              className="group inline-flex items-center gap-1.5 rounded-lg border border-white/10 bg-white/[0.03] px-2.5 py-1.5 text-[10px] font-medium text-slate-300 transition hover:border-violet-500/40 hover:bg-violet-500/10 hover:text-white"
            >
              <Icon
                className={`h-3.5 w-3.5 shrink-0 ${skill.iconClass}`}
                strokeWidth={1.8}
              />

              <span>{skill.name}</span>
            </button>
          );
        })}
      </div>
    </section>
  );
};
