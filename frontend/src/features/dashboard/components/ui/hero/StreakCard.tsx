import { Check, Flame } from "lucide-react";

const weekDays = [
  { label: "M", completed: true },
  { label: "T", completed: true },
  { label: "W", completed: true },
  { label: "T", completed: true },
  { label: "F", completed: false },
  { label: "S", completed: false },
  { label: "S", completed: false },
];

export const StreakCard = () => {
  const streakDays = 1;
  const longestStreak = 12;

  const progress = Math.min((streakDays / 7) * 100, 100);

  return (
    <section className="h-full rounded-xl border border-white/10 bg-[#0b0f17] p-6">
      <div className="flex items-center gap-2">

        <h2 className="text-[12px] font-semibold text-white">
          Your Preparation Streak
        </h2>

        <Flame
          className="h-4 w-4 text-orange-400"
          aria-hidden="true"
        />

      </div>

      <div className="mt-5 flex flex-col gap-6 sm:flex-row sm:items-center ">
        <div
          className="flex h-32 w-32 shrink-0 items-center justify-center self-center rounded-full sm:self-auto"
          style={{
            background: `conic-gradient(
              rgb(139 92 246) ${progress}%,
              rgb(39 35 67) ${progress}% 100%
            )`,
          }}
        >
          <div className="flex h-[106px] w-[106px] flex-col items-center justify-center rounded-full bg-[#0b0f17]">
            <span className="text-3xl font-semibold text-white">
              {streakDays}
            </span>

            <span className="mt-1 text-xs text-slate-400">
              Days
            </span>
          </div>
        </div>

        <div className="min-w-0 flex-1">
          <p className="text-sm text-slate-300">
            Keep it up! You &apos;re doing great.
          </p>

          <div className="mt-4 grid grid-cols-7 gap-2">
            {weekDays.map((day, index) => (
              <div
                key={`${day.label}-${index}`}
                className="flex flex-col items-center gap-2"
              >
                <div
                  className={[
                    "flex h-7 w-7 items-center justify-center rounded-full border",
                    day.completed
                      ? "border-violet-700 bg-violet-700 text-white"
                      : "border-white/10 bg-slate-800 text-slate-500",
                  ].join(" ")}
                >
                  {day.completed && (
                    <Check
                      className="h-3.5 w-3.5"
                      strokeWidth={2.5}
                      aria-hidden="true"
                    />
                  )}
                </div>

                <span className="text-[11px] text-slate-500">
                  {day.label}
                </span>
              </div>
            ))}
          </div>

          <p className="mt-4 text-xs text-slate-500">
            Longest Streak:{" "}
            <span className="font-medium text-slate-300">
              {longestStreak} days
            </span>
          </p>
        </div>
      </div>
    </section>
  );
};
