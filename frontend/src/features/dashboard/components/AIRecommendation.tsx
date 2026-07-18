import {
  ArrowRight,
  Clock3,
  Lightbulb,
  Sparkles,
} from "lucide-react";

export const AIRecommendation = () => {
  return (
    <div className="flex h-full flex-col rounded-xl border border-white/10 bg-[#0b0f17] p-4">

      <div className="flex items-center gap-2">
        <Sparkles
          size={15}
          className="shrink-0 text-yellow-400"
          strokeWidth={2.2}
        />

        <h2 className="text-[11px] font-semibold text-white">
          AI Recommendation
        </h2>
      </div>


      <div className="mt-4 flex flex-1 flex-col rounded-xl border border-yellow-500/40 bg-yellow-500/[0.02] p-4">

        <div className="flex items-start gap-3">
          <Lightbulb
            size={20}
            className="mt-0.5 shrink-0 text-yellow-400"
            strokeWidth={2}
          />

          <p className="min-w-0 text-[11px] leading-5 text-slate-300">
            Based on your resume,{" "}
            <span className="font-semibold text-yellow-400">
              Docker, Redis and REST API
            </span>{" "}
            are missing.
          </p>
        </div>

        <div className="my-4 h-px bg-white/10" />


        <div className="flex flex-1 flex-col">
          <p className="text-[10px] font-medium text-slate-400">
            Recommended Practice
          </p>

          <h3 className="mt-1 text-[14px] font-semibold leading-5 text-white">
            Backend Fundamentals Interview
          </h3>

          <div className="mt-4 flex flex-wrap items-center gap-2">
            <span className="rounded-lg border border-white/10 bg-white/[0.04] px-3 py-1.5 text-[10px] font-medium text-slate-300">
              Intermediate
            </span>

            <span className="inline-flex items-center gap-1.5 rounded-lg border border-white/10 bg-white/[0.04] px-3 py-1.5 text-[10px] font-medium text-slate-300">
              <Clock3 size={12} />
              15 min
            </span>
          </div>


          <button
            type="button"
            className="mt-auto inline-flex w-full items-center justify-center gap-2 rounded-lg bg-violet-600 px-4 py-2.5 text-[11px] font-semibold text-white transition hover:bg-violet-500"
          >
            Start Practice
            <ArrowRight size={15} />
          </button>
        </div>
      </div>
    </div>
  );
};
