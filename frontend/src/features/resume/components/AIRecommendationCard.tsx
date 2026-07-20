import {
    CheckCircle2,
    Lightbulb,
} from "lucide-react";

const recommendations = [
    "Add measurable results to your project descriptions.",
    "Mention REST API development clearly in your experience.",
    "Highlight Docker usage in at least one backend project.",
    "Add Redis and SQL keywords where they genuinely apply.",
];

export const AIRecommendationCard = () => {
    return (
        <div className="rounded-2xl border border-white/10 bg-[#0b0f17] p-6">
            <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-500/10">
                    <Lightbulb className="h-5 w-5 text-violet-400" />
                </div>

                <div>
                    <h2 className="text-lg font-semibold text-white">
                        AI Recommendations
                    </h2>

                    <p className="mt-1 text-sm text-white/50">
                        Improvements that can strengthen your resume.
                    </p>
                </div>
            </div>

            <div className="mt-6 space-y-4">
                {recommendations.map((recommendation) => (
                    <div
                        key={recommendation}
                        className="flex items-start gap-3 rounded-xl border border-white/5 bg-white/[0.02] p-4"
                    >
                        <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-green-400" />

                        <p className="text-sm leading-6 text-white/70">
                            {recommendation}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
};
