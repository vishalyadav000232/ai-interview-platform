import { Link } from "react-router-dom";
import { GrLinkNext } from "react-icons/gr";
import dashboard from "../../../assets/images/dashboard.png";
import { Badge } from "../ui/Badge";
import TrustBadges from "../ui/TrustBadges";

function Hero() {
  return (
    <section className="relative overflow-hidden bg-[#000204] text-white">
      <div className="pointer-events-none absolute left-0 top-0 h-[480px] w-[480px] rounded-full bg-violet-600/20 blur-[150px]" />
      <div className="pointer-events-none absolute right-0 top-28 h-[560px] w-[560px] rounded-full bg-fuchsia-600/10 blur-[160px]" />

      <div className="relative z-10 mx-auto grid min-h-[90vh] max-w-7xl grid-cols-1 items-center gap-14 px-5 py-20 sm:px-6 lg:grid-cols-12 lg:gap-10 lg:px-8">
        {/* Left Content */}
        <div className="order-2 text-center lg:order-1 lg:col-span-5 lg:text-left">
          <Badge>AI Powered Interview Preparation</Badge>

          <h1 className="mt-6 text-4xl font-bold leading-[1.08] tracking-tight sm:text-5xl lg:text-6xl">
            Ace Your{" "}
            <span className="bg-gradient-to-r from-[#5133CA] to-[#B72CFF] bg-clip-text text-transparent">
              Next Interview
            </span>{" "}
            with AI
          </h1>

          <p className="mx-auto mt-6 max-w-xl text-base leading-7 text-gray-400 sm:text-lg lg:mx-0">
            Practice mock interviews, improve your resume, get ATS scores, and
            receive instant AI feedback — all in one platform.
          </p>

          <div className="mt-9 flex flex-col gap-4 sm:flex-row sm:justify-center lg:justify-start">
            <Link
              to="/register"
              className="group inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-[#5133CA] to-[#B72CFF] px-6 py-3.5 font-semibold text-white transition-all duration-300 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-violet-500/30 active:translate-y-0"
            >
              Get Started for Free
              <GrLinkNext className="transition-transform duration-300 group-hover:translate-x-1" />
            </Link>

            <Link
              to="/login"
              className="inline-flex items-center justify-center rounded-xl border border-white/15 bg-white/[0.02] px-6 py-3.5 font-medium text-gray-300 transition-all duration-300 hover:border-white/35 hover:bg-white/[0.05] hover:text-white"
            >
              Login
            </Link>
          </div>

          <TrustBadges />
        </div>

        {/* Right Preview */}
        <div className="order-1 flex justify-center lg:order-2 lg:col-span-7 lg:justify-end">
          <div className="relative w-full max-w-md sm:max-w-xl lg:max-w-[720px]">
            <div className="relative overflow-hidden rounded-[28px] border border-white/10 bg-white/[0.03] p-2 shadow-2xl shadow-violet-500/20 backdrop-blur-xl">
              <img
                src={dashboard}
                alt="InterviewAI dashboard preview"
                className="w-full rounded-[22px] object-cover"
              />

              <div className="pointer-events-none absolute inset-0 rounded-[28px] ring-1 ring-white/10" />
            </div>

            <FloatingCard className="-left-8 top-10">
              <p className="text-xs text-gray-400">AI Score</p>
              <h2 className="mt-1 text-2xl font-bold text-green-400">92%</h2>
              <p className="text-xs text-gray-500">Excellent</p>
            </FloatingCard>

            <FloatingCard className="-right-8 bottom-12">
              <p className="text-xs text-gray-400">ATS Resume</p>
              <h2 className="mt-1 text-2xl font-bold text-violet-400">89%</h2>
              <p className="text-xs text-gray-500">Improved</p>
            </FloatingCard>

            <div className="absolute -left-5 bottom-36 hidden items-center gap-2 rounded-xl border border-white/10 bg-[#0F1117]/90 px-4 py-3 shadow-xl shadow-black/40 backdrop-blur-xl lg:flex">
              <span className="h-2.5 w-2.5 rounded-full bg-green-500 shadow-[0_0_16px_rgba(34,197,94,0.8)]" />
              <span className="text-sm text-gray-200">AI Feedback Ready</span>
            </div>

            <div className="mt-8 grid grid-cols-3 rounded-2xl border border-white/10 bg-white/[0.03] px-5 py-5 text-center backdrop-blur-xl">
              <Stat value="5K+" label="Interviews" />
              <Stat value="95%" label="Success Rate" border />
              <Stat value="50+" label="Companies" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

const FloatingCard = ({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) => {
  return (
    <div
      className={`absolute hidden rounded-2xl border border-white/10 bg-[#0F1117]/90 p-4 shadow-xl shadow-black/40 backdrop-blur-xl lg:block ${className}`}
    >
      {children}
    </div>
  );
};

const Stat = ({
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
      <h3 className="text-2xl font-bold text-white">{value}</h3>
      <p className="mt-1 text-xs text-gray-400 sm:text-sm">{label}</p>
    </div>
  );
};

export default Hero;