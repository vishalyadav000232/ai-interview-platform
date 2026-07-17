import { ArrowRight, Clock3, Rocket, Sparkles } from "lucide-react";

export const RecommendationCard = () => {
  return (
    <div className="flex h-full items-center justify-between gap-8 rounded-3xl border border-white/10 bg-[#0b0f17] p-4">

      <div className="flex items-center gap-6">
        <div className="flex h-28 w-28 items-center justify-center rounded-full bg-violet-600/1">
          <Rocket
            className="h-16 w-16 rotate-[-20deg] text-violet-400"
            strokeWidth={1.8}
          />
        </div>

        <div className="space-y-4">
          <span className="inline-flex items-center gap-2 rounded-full bg-violet-600/10 px-3 py-1 text-xs font-medium uppercase tracking-wide text-violet-300">
            <Sparkles className="h-3.5 w-3.5" />
            Next Recommendation
          </span>

          <div>
            <h2 className="text-m font-semibold text-white">
              FastAPI Backend Mock Interview
            </h2>

            <p className="mt-1 text-[12px] text-slate-400">
              Based on your resume and weak areas
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 rounded-lg border border-white/10 px-2 py-1 text-[12px] text-slate-300">
              <Clock3 className="h-3 w-3" />
              12 min
            </div>

            <div className="rounded-lg border border-white/10 px-2 py-1 text-[12px] text-slate-300">
               🙂 Intermediate
            </div>
          </div>
        </div>
      </div>

      {/* Right */}
      <button
        type="button"
        className="flex shrink-0 items-center gap-2 rounded-xl bg-violet-600 px-5 py-3 text-base font-semibold text-white transition hover:bg-violet-500"
      >
        Start Interview

        <ArrowRight className="h-5 w-5 transition-all transform " />
      </button>
    </div>
  );
};
