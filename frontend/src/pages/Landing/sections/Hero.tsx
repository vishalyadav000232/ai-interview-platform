
import { Link } from "react-router-dom";

function Hero() {
  return (
    <section className="bg-black text-white">
      <div className="mx-auto flex min-h-[90vh] max-w-7xl items-center justify-between px-6">

        {/* Left Side */}
        <div className="max-w-2xl">

          <span className="rounded-full border border-violet-500 px-4 py-2 text-sm text-violet-400">
            🚀 AI Powered Interview Preparation
          </span>

          <h1 className="mt-6 text-6xl font-bold leading-tight">
            Ace Your
            <span className="text-violet-500"> Next Interview </span>
            with AI
          </h1>

          <p className="mt-6 text-lg text-gray-400">
            Practice mock interviews, improve your resume,
            receive ATS scores, and get instant AI feedback.
          </p>

          <div className="mt-10 flex gap-4">
            <Link
              to="/register"
              className="rounded-xl bg-violet-600 px-6 py-3 font-medium"
            >
              Get Started
            </Link>

            <Link
              to="/login"
              className="rounded-xl border border-gray-700 px-6 py-3"
            >
              Login
            </Link>
          </div>

        </div>

        {/* Right Side */}

        <div className="hidden lg:flex h-[500px] w-[500px] items-center justify-center rounded-3xl border border-white/10 bg-zinc-900">

          Dashboard Preview

        </div>

      </div>
    </section>
  );
}

export default Hero;