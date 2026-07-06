import { GrLinkNext } from "react-icons/gr"
import { Link } from "react-router-dom"


export const CTA = () => {
  return (
    <section className=" bg-[#000204] py-24">


  <div className="mx-auto max-w-5xl rounded-3xl border border-white/1  to-fuchsia-500/1 backdrop-blur-2xl px-8 py-20 text-center">

    <h2 className="text-4xl font-bold text-white">
      Ready to Ace Your{" "}
      <span className="bg-gradient-to-r from-violet-500 to-fuchsia-500 bg-clip-text text-transparent">
        Next Interview?
      </span>
    </h2>

    <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-400">
      Practice with AI-powered mock interviews, improve your resume,
      and receive personalized feedback before your real interview.
    </p>

    <div className="mt-10 flex flex-col justify-center gap-4 sm:flex-row">
       <Link
                to="/register"
                className="group inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-[#5133CA] to-[#B72CFF] px-6 py-3 font-medium text-white transition-all duration-300 hover:shadow-lg hover:shadow-violet-500/30"
              >
                Get Started for Free
                <GrLinkNext className="transition-transform duration-300 group-hover:translate-x-1" />
              </Link>

      <button className="rounded-xl border border-white/10 px-8 py-4 font-semibold text-white transition hover:border-violet-500">
        ▶ Watch Demo
      </button>
    </div>

    <p className="mt-6 text-sm text-gray-500">
      No Credit Card Required • Free Forever • Setup in 2 Minutes
    </p>

  </div>
</section>
  )
}
