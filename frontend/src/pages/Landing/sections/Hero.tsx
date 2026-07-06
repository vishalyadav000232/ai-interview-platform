import { Link } from "react-router-dom";
import { GrLinkNext } from "react-icons/gr";
import dashboard from "../../../assets/images/dashboard.png";
import { Badge } from "../ui/Badge";
import TrustBadges from "../ui/TrustBadges";

function Hero() {
  return (
    <section className="relative overflow-hidden bg-[#000204] text-white">
      <div className="mx-auto grid min-h-[90vh] max-w-7xl grid-cols-1 items-center gap-16 px-5 py-20 lg:grid-cols-12 lg:px-6">
        
        <div className="relative order-2 text-center lg:order-1 lg:col-span-5 lg:text-left">
          <div className="absolute -left-24 top-10 -z-0 h-[420px] w-[420px] rounded-full bg-violet-600/20 blur-[140px]" />

          <div className="relative z-10">
            <Badge>AI Powered Interview Preparation</Badge>

            <h1 className="mt-6 text-4xl font-bold leading-tight sm:text-5xl lg:text-6xl">
              Ace Your{" "}
              <span className="bg-gradient-to-r from-[#5133CA] to-[#B72CFF] bg-clip-text text-transparent">
                Next Interview
              </span>{" "}
              with AI
            </h1>

            <p className="mx-auto mt-6 max-w-xl text-base leading-7 text-gray-400 sm:text-lg lg:mx-0">
              Practice mock interviews, improve your resume, receive ATS scores,
              and get instant AI feedback.
            </p>

            <div className="mt-10 flex flex-col gap-4 sm:flex-row sm:justify-center lg:justify-start">
              <Link
                to="/register"
                className="group inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-[#5133CA] to-[#B72CFF] px-6 py-3 font-medium text-white transition-all duration-300 hover:shadow-lg hover:shadow-violet-500/30"
              >
                Get Started for Free
                <GrLinkNext className="transition-transform duration-300 group-hover:translate-x-1" />
              </Link>

              <Link
                to="/login"
                className="rounded-xl border border-white/15 px-6 py-3 text-center text-gray-300 transition hover:border-white/40 hover:text-white"
              >
                Login
              </Link>
            </div>

            <TrustBadges />
          </div>
        </div>

        <div className="relative order-1 flex justify-center lg:order-2 lg:col-span-7 lg:justify-end">
          <div className="absolute -right-20 top-10 h-[500px] w-[500px] rounded-full bg-violet-600/20 blur-[140px]" />

          <div className="relative z-10 w-full max-w-md sm:max-w-xl lg:max-w-[720px]">
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-zinc-900/70 shadow-2xl shadow-violet-500/20 backdrop-blur-xl">
              <img
                src={dashboard}
                alt="InterviewAI Dashboard Preview"
                className="w-full rounded-3xl object-cover"
              />
            </div>

            <div className="absolute -left-8 top-10 hidden rounded-2xl border border-white/10 bg-[#0F1117]/90 p-4 shadow-xl backdrop-blur-xl lg:block">
              <p className="text-xs text-gray-400">AI Score</p>
              <h2 className="mt-1 text-2xl font-bold text-green-400">92%</h2>
              <p className="text-xs text-gray-500">Excellent</p>
            </div>

            <div className="absolute -right-8 bottom-10 hidden rounded-2xl border border-white/10 bg-[#0F1117]/90 p-4 shadow-xl backdrop-blur-xl lg:block">
              <p className="text-xs text-gray-400">ATS Resume</p>
              <h2 className="mt-1 text-2xl font-bold text-violet-400">89%</h2>
              <p className="text-xs text-gray-500">Improved</p>
            </div>

            <div className="absolute -left-5 bottom-36 hidden items-center gap-2 rounded-xl border border-white/10 bg-[#0F1117]/90 px-4 py-3 shadow-xl backdrop-blur-xl lg:flex">
              <span className="h-3 w-3 rounded-full bg-green-500"></span>
              <span className="text-sm text-gray-200">AI Feedback Ready</span>
            </div>

            <div className="mt-8 flex items-center justify-center gap-8 text-sm text-gray-400 lg:justify-center">
              <div>
                <h3 className="text-2xl font-bold text-white">5K+</h3>
                <p>Interviews</p>
              </div>

              <div className="h-10 w-px bg-white/10"></div>

              <div>
                <h3 className="text-2xl font-bold text-white">95%</h3>
                <p>Success Rate</p>
              </div>

              <div className="h-10 w-px bg-white/10"></div>

              <div>
                <h3 className="text-2xl font-bold text-white">50+</h3>
                <p>Companies</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>
  );
}

export default Hero;