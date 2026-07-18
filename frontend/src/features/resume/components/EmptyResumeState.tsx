import {
    BarChart3,
    FileSearch,
    Lightbulb,
    Target,
    UploadCloud,
} from "lucide-react";
type EmptyResumeStateProps = {
    onUploadClick: () => void;
};
const resumeFeatures = [
    {
        title: "ATS Score & Insights",
        description: "Know how strong your resume is.",
        icon: BarChart3,
    },
    {
        title: "Keyword Match",
        description: "See how well your resume matches job requirements.",
        icon: FileSearch,
    },
    {
        title: "Missing Skills",
        description: "Discover the skills you should improve.",
        icon: Target,
    },
    {
        title: "AI Feedback",
        description: "Get personalised suggestions to improve your resume.",
        icon: Lightbulb,
    },
];

export const EmptyResumeState = ({
    onUploadClick,
}: EmptyResumeStateProps) => {


    return (
        <section className="space-y-6">
            {/* Main empty-state card */}
            <div className="flex min-h-[420px] flex-col items-center justify-center rounded-2xl border border-dashed border-violet-500/40 bg-[#0b0f17] px-6 py-12 text-center">
                <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-violet-500/10 text-violet-400">
                    <UploadCloud
                        className="h-10 w-10"
                        aria-hidden="true"
                    />
                </div>

                <h2 className="mt-6 text-xl font-semibold text-white sm:text-2xl">
                    No Resume Uploaded Yet
                </h2>

                <p className="mt-3 max-w-xl text-sm leading-6 text-slate-400">
                    Upload your resume to unlock ATS analysis, missing skills,
                    AI-powered feedback and personalised mock interview recommendations.
                </p>

                <button
                    type="button"
                    onClick={onUploadClick}
                    className="mt-7 inline-flex items-center justify-center gap-2 rounded-xl bg-violet-600 px-5 py-3 text-sm font-semibold text-white transition-colors hover:bg-violet-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-400"
                >
                    <UploadCloud className="h-4 w-4" />
                    Upload Your Resume
                </button>

                <p className="mt-4 text-xs text-slate-500">
                    Supported formats: PDF, DOCX · Maximum size: 5MB
                </p>
            </div>


            <div>
                <h3 className="text-sm font-semibold text-white">
                    What you&apos;ll get after upload
                </h3>

                <div className="mt-4 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                    {resumeFeatures.map((feature) => {
                        const Icon = feature.icon;

                        return (
                            <article
                                key={feature.title}
                                className="rounded-xl border border-white/10 bg-[#0b0f17] p-5"
                            >
                                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-500/10 text-violet-400">
                                    <Icon
                                        className="h-5 w-5"
                                        aria-hidden="true"
                                    />
                                </div>

                                <h4 className="mt-4 text-sm font-semibold text-white">
                                    {feature.title}
                                </h4>

                                <p className="mt-2 text-xs leading-5 text-slate-400">
                                    {feature.description}
                                </p>
                            </article>
                        );
                    })}
                </div>
            </div>
        </section>
    );
};
