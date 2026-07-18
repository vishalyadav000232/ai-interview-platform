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

  const radius = 46;

  const circumference = 2 * Math.PI * radius;

  const progressPercentage = Math.min(
    (streakDays / 7) * 100,
    100
  );

  const strokeOffset =
    circumference -
    (progressPercentage / 100) * circumference;

  return (
    <section className="h-full rounded-xl border border-white/10 bg-[#0b0f17] p-5">

      <div className="flex items-center gap-2">
        <h2 className="text-[11px] font-semibold text-white">
          Your Preparation Streak
        </h2>

        <Flame
          className="h-4 w-4 text-orange-400"
          aria-hidden="true"
        />
      </div>


      <div className="mt-5 flex flex-col gap-6 sm:flex-row sm:items-center">

        <div className="relative h-28 w-28 shrink-0 self-center sm:self-auto">
          <svg
            className="-rotate-90"
            width="112"
            height="112"
            viewBox="0 0 112 112"
          >

            <circle
              cx="56"
              cy="56"
              r={radius}
              fill="none"
              stroke="rgba(255,255,255,0.08)"
              strokeWidth="8"
            />


            <circle
              cx="56"
              cy="56"
              r={radius}
              fill="none"
              stroke="#8b5cf6"
              strokeWidth="8"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={strokeOffset}
              className="transition-all duration-700"
            />
          </svg>


          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-2xl font-semibold leading-none text-white">
              {streakDays}
            </span>

            <span className="mt-1 text-[11px] text-slate-400">
              Days
            </span>
          </div>
        </div>


        <div className="min-w-0 flex-1">
          <p className="text-[11px] text-slate-300">
            Keep it up! You&apos;re doing great.
          </p>


          <div className="mt-4 grid grid-cols-7 gap-2">
            {weekDays.map((day, index) => (
              <div
                key={`${day.label}-${index}`}
                className="flex flex-col items-center gap-2"
              >
                <div
                  className={[
                    "flex h-5 w-5 items-center justify-center rounded-full border",
                    day.completed
                      ? "border-violet-600 bg-violet-600 text-white"
                      : "border-white/10 bg-slate-800 text-slate-500",
                  ].join(" ")}
                >
                  {day.completed && (
                    <Check
                      className="h-3 w-3"
                      strokeWidth={2.5}
                      aria-hidden="true"
                    />
                  )}
                </div>

                <span className="text-[10px] text-slate-500">
                  {day.label}
                </span>
              </div>
            ))}
          </div>

          
          <p className="mt-4 text-[11px] text-slate-500">
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
