
import { ArrowRight } from "lucide-react";

const skills = [
  {
    name: "Python",
    score: 85,
    barClass: "bg-emerald-500",
  },
  {
    name: "FastAPI",
    score: 78,
    barClass: "bg-blue-500",
  },
  {
    name: "PostgreSQL",
    score: 72,
    barClass: "bg-violet-500",
  },
  {
    name: "Docker",
    score: 42,
    barClass: "bg-orange-400",
  },
  {
    name: "Redis",
    score: 35,
    barClass: "bg-red-500",
  },
  {
    name: "REST API",
    score: 60,
    barClass: "bg-cyan-400",
  },
  {
    name: "JWT / Auth",
    score: 50,
    barClass: "bg-yellow-400",
  },
];

export const SkillsProgress = () => {
  return (
    <section className="h-full rounded-xl border border-white/10 bg-[#0b0f17] p-4">
     
      <div className="flex items-center justify-between">
        <h2 className="text-[11px] font-semibold text-white">
          Skills Progress
        </h2>

        <button
          type="button"
          className="group inline-flex items-center gap-1 text-[10px] font-medium text-violet-400 transition hover:text-violet-300"
        >
          View All Skills

          <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
        </button>
      </div>


      <div className="mt-5 space-y-4">
        {skills.map((skill) => (
          <div
            key={skill.name}
            className="grid grid-cols-[68px_minmax(0,1fr)_34px] items-center gap-3"
          >

            <p className="truncate text-[10px] font-medium text-slate-300">
              {skill.name}
            </p>


            <div className="h-1.5 overflow-hidden rounded-full bg-white/10">
              <div
                className={`h-full rounded-full transition-all duration-700 ${skill.barClass}`}
                style={{
                  width: `${skill.score}%`,
                }}
              />
            </div>


            <span className="text-right text-[10px] font-medium text-slate-300">
              {skill.score}%
            </span>
          </div>
        ))}
      </div>
    </section>
  );
};
