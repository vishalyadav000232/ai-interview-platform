import { Link } from "react-router-dom";
import dashboard from "../../../assets/images/dashboard.png";
import { Badge } from "../ui/Badge";
import { GrLinkNext } from "react-icons/gr";

function Hero() {
    return (
        <section className="bg-[#000204] text-white">
            <div className="mx-auto grid min-h-[90vh] max-w-7xl grid-cols-1 items-center gap-16 px-5 py-20 lg:grid-cols-12 lg:px-6">

                <div className="order-2 text-center lg:order-1 lg:col-span-5 lg:text-left">
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
                            className="group inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-[#5133CA] to-[#B72CFF] px-6 py-3 font-medium text-white transition-all duration-300 hover:shadow-lg hover:shadow-violet-500/30"
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
                </div>
                <div className="order-1 flex justify-center lg:order-2 lg:col-span-7 lg:justify-end">
                    <div className="w-full max-w-md rounded-lg border border-white/10  shadow-2xl shadow-violet-500/10 sm:max-w-xl lg:max-w-[720px] ">
                        <img
                            src={dashboard}
                            alt="InterviewAI Dashboard Preview"
                            className="w-full rounded-3xl object-cover"
                        />
                    </div>
                </div>

            </div>
        </section>
    );
}

export default Hero;