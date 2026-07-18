
import { CheckCircle2 } from "lucide-react";

const goals = [
  {
    title: "Complete 1 Mock Interview",
    completed: false,
  },
  {
    title: "Practice 15 Questions",
    completed: true,
  },
  {
    title: "Improve SQL Skills",
    completed: true,
  },
];

export const TodayGoal = () => {
  const completedGoals = goals.filter(
    (goal) => goal.completed,
  ).length;

  const totalGoals = goals.length;

  const progress =
    (completedGoals / totalGoals) * 100;

  const radius = 38;

  const circumference = 2 * Math.PI * radius;

  const strokeOffset =
    circumference -
    (progress / 100) * circumference;

  return (
    <section className="rounded-xl border border-white/10 bg-[#0b0f17] p-4">

      <h2 className="text-[11px] font-semibold text-white">
        Today's Goal
      </h2>

      <div className="mt-5 flex items-center justify-between gap-6">

        <div className="flex-1 space-y-4">
          {goals.map((goal) => (
            <div
              key={goal.title}
              className="flex items-center gap-3"
            >
              {goal.completed ? (
                <CheckCircle2
                  className="h-5 w-5 shrink-0 text-emerald-400"
                  strokeWidth={2}
                />
              ) : (
                <div className="h-5 w-5 rounded-full border border-white/20" />
              )}

              <span
                className={`text-[11px] ${goal.completed
                    ? "text-slate-200"
                    : "text-slate-400"
                  }`}
              >
                {goal.title}
              </span>
            </div>
          ))}
        </div>


        <div className="relative h-24 w-24 shrink-0">
          <svg
            width="96"
            height="96"
            viewBox="0 0 96 96"
            className="-rotate-90"
          >

            <circle
              cx="48"
              cy="48"
              r={radius}
              fill="none"
              stroke="rgba(255,255,255,0.08)"
              strokeWidth="7"
            />


            <circle
              cx="48"
              cy="48"
              r={radius}
              fill="none"
              stroke="#8b5cf6"
              strokeWidth="7"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={strokeOffset}
              className="transition-all duration-700"
            />
          </svg>

          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-2xl font-semibold text-white">
              {completedGoals}
              <span className="text-base text-slate-500">
                /{totalGoals}
              </span>
            </span>

            <span className="text-[10px] text-slate-400">
              Completed
            </span>
          </div>
        </div>
      </div>

      
      <div className="mt-5 border-t border-white/10 pt-4">
        <p className="text-[11px] font-medium text-emerald-400">
          You're on the right track! 🚀
        </p>
      </div>
    </section>
  );
};
