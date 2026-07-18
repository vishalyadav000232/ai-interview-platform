import { ArrowRight } from "lucide-react";
import { ProgressRing } from "./ui/ResumeAnalytics/CircularProgress";

export const ResumeAnalysis = () => {
  const resume = {
    completeness: 78,
    keywordMatch: 60,
    matchedSkills: 6,
    missingSkills: 4,
    skills: ["Docker", "Redis", "REST API", "SQL", "Python"],
  };


  const visibleSkills = resume.skills.slice(0, 4);
  const remainingSkills = resume.skills.length - 4;


  return (
    <section className="h-full rounded-xl border border-white/10 bg-[#0b0f17] p-4">

      <div className="flex items-center justify-between">
        <h2 className="text-xs font-semibold text-white sm:text-sm">
          Resume Analysis
        </h2>

        <button
          type="button"
          className="group inline-flex items-center gap-1 text-xs font-medium text-violet-400 transition-colors hover:text-violet-300"
        >
          View Full Analysis

          <ArrowRight
            className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5"
            aria-hidden="true"
          />
        </button>
      </div>


      <div className="mt-5 grid grid-cols-2">
        <div className="flex justify-center border-r border-white/10 px-3">
          <ProgressRing
            value={resume.completeness}
            label="Completeness"
            color="#22c55e"
          />
        </div>

        <div className="flex justify-center px-3">
          <ProgressRing
            value={resume.keywordMatch}
            label="Keyword Match"
            color="#8b5cf6"
          />
        </div>
      </div>


      <div className="mt-4 grid grid-cols-2 border-y border-white/10 py-1">
        <div className=" flex items-center justify-around border-r border-white/10 pr-4">
          <p className="text-xs text-slate-500">
            Matched Skills
          </p>

          <p className="mt-1 text-lg font-semibold text-emerald-400">
            {resume.matchedSkills}
          </p>
        </div>

        <div className=" flex items-center justify-around" >
          <p className="text-xs text-slate-500">
            Missing Skills
          </p>

          <p className="mt-1 text-lg font-semibold text-orange-400">
            {resume.missingSkills}
          </p>
        </div>
      </div>


      <div className="mt-1">
        <p className="text-xs text-slate-500">
          Missing Skills Preview
        </p>

        <div className="mt-2 flex flex-wrap gap-2">
          {visibleSkills.map((skill) => (
            <span
              key={skill}
              className="rounded-full border border-white/10 bg-white/[0.03] px-2.5 py-1 text-[11px] font-medium text-slate-300"
            >
              {skill}
            </span>
          ))}

          {remainingSkills > 0 && (
            <span className="rounded-full border border-violet-500/20 bg-violet-500/10 px-2.5 py-1 text-[11px] font-medium text-violet-400">
              +{remainingSkills} More
            </span>
          )}
        </div>
      </div>
    </section>
  );
};
