import { ArrowUpRight, Target } from "lucide-react";

export const ATSScoreCard = () => {
    const atsScore = 78;

    return (
        <div className="rounded-2xl border border-white/10 bg-[#0b0f17] p-6">
            <div className="grid gap-8 lg:grid-cols-[220px_1fr] lg:items-center">
                <div className="flex justify-center">
                    <div className="relative flex h-44 w-44 items-center justify-center rounded-full border-[12px] border-violet-500/20">
                        <div className="absolute inset-[-12px] rounded-full border-[12px] border-transparent border-t-violet-500 border-r-violet-500" />

                        <div className="text-center">
                            <p className="text-4xl font-bold text-white">
                                {atsScore}
                            </p>

                            <p className="text-sm text-white/50">
                                out of 100
                            </p>
                        </div>
                    </div>
                </div>

                <div>
                    <div className="flex items-center gap-2">
                        <Target className="h-5 w-5 text-violet-400" />

                        <p className="text-sm font-medium text-violet-400">
                            ATS Compatibility Score
                        </p>
                    </div>

                    <h2 className="mt-3 text-2xl font-semibold text-white">
                        Your resume is in a good position
                    </h2>

                    <p className="mt-2 max-w-2xl text-sm leading-6 text-white/50">
                        Your resume contains strong backend skills and relevant
                        projects. A few keyword and formatting improvements can
                        increase your chances of passing ATS screening.
                    </p>

                    <div className="mt-5 inline-flex items-center gap-2 rounded-full bg-green-500/10 px-3 py-1.5 text-sm font-medium text-green-400">
                        <ArrowUpRight className="h-4 w-4" />
                        Good resume score
                    </div>
                </div>
            </div>
        </div>
    );
};
