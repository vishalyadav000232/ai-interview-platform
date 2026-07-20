import { Download, FileText } from "lucide-react";

export const ResumeHeader = () => {
    return (
        <div className="flex flex-col gap-4 rounded-2xl border border-white/10 bg-[#0b0f17] p-6 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex items-center gap-4">
                <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-violet-500/10">
                    <FileText className="h-7 w-7 text-violet-400" />
                </div>

                <div>
                    <h1 className="text-2xl font-semibold text-white">
                        Resume Analysis
                    </h1>

                    <div className="mt-2 flex flex-wrap items-center gap-3 text-sm text-white/60">
                        <span>Backend_Resume.pdf</span>

                        <span className="rounded-full bg-green-500/10 px-2.5 py-1 text-xs font-medium text-green-400">
                            Active
                        </span>

                        <span>Uploaded 2 minutes ago</span>
                    </div>
                </div>
            </div>

            <button className="inline-flex items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-sm font-medium text-white transition hover:bg-white/10">
                <Download className="h-4 w-4" />
                Download Report
            </button>
        </div>
    );
};
