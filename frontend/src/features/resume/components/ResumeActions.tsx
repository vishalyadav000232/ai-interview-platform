import {
    ArrowRight,
    Download,
    RefreshCcw,
} from "lucide-react";

export const ResumeActions = () => {
    return (
        <div className="rounded-2xl border border-white/10 bg-[#0b0f17] p-6">
            <div className="flex flex-col gap-2">
                <h2 className="text-xl font-semibold text-white">
                    Ready for Your Next Step?
                </h2>

                <p className="text-sm text-white/50">
                    Your resume has been analyzed. Continue improving your profile
                    or start practicing interviews.
                </p>
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-3">
                <button className="flex items-center justify-center gap-2 rounded-xl bg-violet-600 px-5 py-3 font-medium text-white transition hover:bg-violet-500">
                    <ArrowRight className="h-5 w-5" />
                    Start AI Interview
                </button>

                <button className="flex items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-5 py-3 font-medium text-white transition hover:bg-white/10">
                    <RefreshCcw className="h-5 w-5" />
                    Replace Resume
                </button>

                <button className="flex items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-5 py-3 font-medium text-white transition hover:bg-white/10">
                    <Download className="h-5 w-5" />
                    Download Report
                </button>
            </div>
        </div>
    );
};
