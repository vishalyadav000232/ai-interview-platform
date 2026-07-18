import {
  ArrowRight,
  Code2,
  Database,
  GitBranch,
  Server,
} from "lucide-react";

const recentInterviews = [
  {
    id: 1,
    title: "FastAPI Backend Interview",
    date: "May 18, 2025",
    duration: "12 min",
    score: 82,
    icon: Server,
    iconStyle: "bg-blue-500/10 text-blue-400",
  },
  {
    id: 2,
    title: "Database & SQL Interview",
    date: "May 15, 2025",
    duration: "15 min",
    score: 74,
    icon: Database,
    iconStyle: "bg-cyan-500/10 text-cyan-400",
  },
  {
    id: 3,
    title: "System Design Basics",
    date: "May 12, 2025",
    duration: "20 min",
    score: 68,
    icon: GitBranch,
    iconStyle: "bg-emerald-500/10 text-emerald-400",
  },
  {
    id: 4,
    title: "Behavioral Interview",
    date: "May 10, 2025",
    duration: "10 min",
    score: 88,
    icon: Code2,
    iconStyle: "bg-violet-500/10 text-violet-400",
  },
];

const getScoreColor = (score: number) => {
  if (score >= 80) {
    return "text-emerald-400";
  }

  if (score >= 70) {
    return "text-yellow-400";
  }

  return "text-orange-400";
};

const getScoreStroke = (score: number) => {
  if (score >= 80) {
    return "#22c55e";
  }

  if (score >= 70) {
    return "#eab308";
  }

  return "#f97316";
};

type ScoreRingProps = {
  score: number;
};

const ScoreRing = ({ score }: ScoreRingProps) => {
  const radius = 16;
  const circumference = 2 * Math.PI * radius;

  const strokeOffset =
    circumference - (score / 100) * circumference;

  return (
    <div className="relative h-10 w-10 shrink-0">
      <svg
        width="40"
        height="40"
        viewBox="0 0 40 40"
        className="-rotate-90"
      >

        <circle
          cx="20"
          cy="20"
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.08)"
          strokeWidth="3"
        />


        <circle
          cx="20"
          cy="20"
          r={radius}
          fill="none"
          stroke={getScoreStroke(score)}
          strokeWidth="3"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={strokeOffset}
          className="transition-all duration-700"
        />
      </svg>

      <span
        className={`absolute inset-0 flex items-center justify-center text-[9px] font-semibold ${getScoreColor(
          score,
        )}`}
      >
        {score}%
      </span>
    </div>
  );
};

export const RecentInterviews = () => {
  return (
    <section className="h-full rounded-xl border border-white/10 bg-[#0b0f17] p-4">

      <div className="flex items-center justify-between">
        <h2 className="text-[11px] font-semibold text-white">
          Recent Interviews
        </h2>

        <button
          type="button"
          className="group inline-flex items-center gap-1 text-[10px] font-medium text-violet-400 transition hover:text-violet-300"
        >
          View All

          <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
        </button>
      </div>

      <div className="mt-4">
        {recentInterviews.map((interview, index) => {
          const Icon = interview.icon;

          return (
            <button
              key={interview.id}
              type="button"
              className={[
                "group flex w-full items-center gap-3 py-3 text-left",
                index !== recentInterviews.length - 1
                  ? "border-b border-white/10"
                  : "",
              ].join(" ")}
            >
           
              <div
                className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ${interview.iconStyle}`}
              >
                <Icon
                  className="h-4.5 w-4.5"
                  strokeWidth={1.8}
                />
              </div>


              <div className="min-w-0 flex-1">
                <h3 className="truncate text-[11px] font-medium text-slate-200 transition group-hover:text-white">
                  {interview.title}
                </h3>

                <div className="mt-1 flex items-center gap-1.5 text-[9px] text-slate-500">
                  <span>{interview.date}</span>

                  <span className="h-1 w-1 rounded-full bg-slate-600" />

                  <span>{interview.duration}</span>
                </div>
              </div>


              <ScoreRing score={interview.score} />


              <ArrowRight className="h-4 w-4 shrink-0 text-slate-600 transition group-hover:translate-x-0.5 group-hover:text-slate-300" />
            </button>
          );
        })}
      </div>
    </section>
  );
};
