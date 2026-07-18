import {
  ArrowRight,
  Clock3,
  Rocket,
  Sparkles,
  UserRound,
} from "lucide-react";

export const RecommendationCard = () => {
  return (
    <div className="flex h-full flex-col gap-5 rounded-xl border border-white/10 bg-[#0b0f17] p-5 lg:flex-row lg:items-center lg:justify-between">

      <div className="flex min-w-0 items-center gap-5">

        <div className="flex h-24 w-24 shrink-0 items-center justify-center rounded-full bg-violet-600/10">
          <Rocket
            className="h-14 w-14 -rotate-[20deg] text-violet-400"
            strokeWidth={1.8}
          />
        </div>


        <div className="min-w-0">
          <span className="inline-flex items-center gap-2 rounded-full bg-violet-600/10 px-3 py-1 text-[10px] font-medium uppercase tracking-wide text-violet-300">
            <Sparkles className="h-3.5 w-3.5 shrink-0" />
            Next Recommendation
          </span>

          <div className="mt-4">
            <h2 className="text-sm font-semibold text-white sm:text-base">
              FastAPI Backend Mock Interview
            </h2>

            <p className="mt-1 text-[11px] leading-5 text-slate-400">
              Based on your resume and weak areas
            </p>
          </div>


          <div className="mt-4 flex flex-wrap items-center gap-2">
            <span className="inline-flex items-center gap-1.5 rounded-lg border border-white/10 bg-white/[0.02] px-2.5 py-1.5 text-[10px] text-slate-300">
              <Clock3 className="h-3.5 w-3.5 shrink-0" />
              12 min
            </span>

            <span className="inline-flex items-center gap-1.5 rounded-lg border border-white/10 bg-white/[0.02] px-2.5 py-1.5 text-[10px] text-slate-300">
              <UserRound className="h-3.5 w-3.5 shrink-0" />
              Intermediate
            </span>
          </div>
        </div>
      </div>

      <button
        type="button"
        className="group inline-flex w-full shrink-0 items-center justify-center gap-2 rounded-xl bg-violet-600 px-5 py-3 text-[12px] font-semibold text-white transition hover:bg-violet-500 lg:w-auto"
      >
        Start Interview

        <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
      </button>
    </div>
  );
};
