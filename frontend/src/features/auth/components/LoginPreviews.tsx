import { Bot, FileText, TrendingUp } from "lucide-react";
import type { ReactNode } from "react";

export const LoginPreview = () => {
  return (
    <div className="relative w-full">
      <div className="pointer-events-none absolute left-1/2 top-0 h-72 w-72 -translate-x-1/2 rounded-full bg-violet-600/20 blur-3xl" />

      <div className="relative overflow-hidden rounded-[32px] border border-white/10 bg-white/[0.03] p-8 shadow-[0_20px_80px_rgba(139,92,246,0.16)] backdrop-blur-xl">
        <div className="relative rounded-2xl border border-white/10 bg-[#090917] p-5">
          <div className="mb-4 flex gap-2">
            <span className="h-2 w-2 rounded-full bg-violet-400" />
            <span className="h-2 w-2 rounded-full bg-violet-400/60" />
            <span className="h-2 w-2 rounded-full bg-violet-400/30" />
          </div>

          <div className="flex items-center gap-5">
            <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-2xl bg-violet-600/20">
              <Bot className="h-10 w-10 text-violet-400" />
            </div>

            <div className="min-w-0 flex-1 space-y-3">
              <div className="h-3 w-3/4 rounded-full bg-white/10" />
              <div className="h-3 w-1/2 rounded-full bg-white/10" />
              <div className="h-10 rounded-xl bg-violet-500/10" />
            </div>
          </div>
        </div>

        <div className="relative mt-8 grid grid-cols-3 rounded-2xl border border-white/10 bg-white/[0.03] p-5 text-center">
          <Score value="86%" label="Interview Score" />
          <Score value="91%" label="ATS Resume" border />
          <Score value="88%" label="Communication" />
        </div>

        <div className="relative mt-10 text-center">
          <h2 className="text-4xl font-bold leading-tight">
            Practice <span className="text-violet-500">Smarter,</span>
            <br />
            Get Hired <span className="text-violet-500">Faster.</span>
          </h2>

          <p className="mx-auto mt-4 max-w-md text-sm leading-6 text-gray-400">
            AI-powered mock interviews, personalized feedback, and smart resume
            analysis — all in one place.
          </p>
        </div>

        <div className="relative mt-10 grid grid-cols-3 gap-5">
          <Feature
            icon={<Bot />}
            title="AI Mock Interviews"
            desc="Real-time voice practice"
          />

          <Feature
            icon={<FileText />}
            title="ATS Resume Analysis"
            desc="Improve resume score"
          />

          <Feature
            icon={<TrendingUp />}
            title="Detailed Feedback"
            desc="Actionable insights"
          />
        </div>
      </div>
    </div>
  );
};

const Score = ({
  value,
  label,
  border = false,
}: {
  value: string;
  label: string;
  border?: boolean;
}) => {
  return (
    <div className={border ? "border-x border-white/10" : ""}>
      <h3 className="text-3xl font-bold text-white">{value}</h3>
      <p className="mt-2 text-xs text-gray-400">{label}</p>
    </div>
  );
};

const Feature = ({
  icon,
  title,
  desc,
}: {
  icon: ReactNode;
  title: string;
  desc: string;
}) => {
  return (
    <div className="min-w-0">
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-violet-600/20 text-violet-400">
        {icon}
      </div>

      <h4 className="text-sm font-semibold text-white">{title}</h4>
      <p className="mt-2 text-xs leading-5 text-gray-400">{desc}</p>
    </div>
  );
};