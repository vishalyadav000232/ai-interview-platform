import {
    BriefcaseBusiness,
    CheckCircle2,
    FileCheck2,
    FolderKanban,
    Target,
    Wrench,
} from "lucide-react";

const metrics = [
    {
        label: "Resume Completeness",
        value: "78%",
        icon: FileCheck2,
    },
    {
        label: "Keyword Match",
        value: "60%",
        icon: Target,
    },
    {
        label: "Skills Score",
        value: "18/25",
        icon: Wrench,
    },
    {
        label: "Projects Score",
        value: "20/25",
        icon: FolderKanban,
    },
    {
        label: "Experience Score",
        value: "15/25",
        icon: BriefcaseBusiness,
    },
    {
        label: "ATS Status",
        value: "Good",
        icon: CheckCircle2,
    },
];

export const MetricsGrid = () => {
    return (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {metrics.map((metric) => {
                const Icon = metric.icon;

                return (
                    <div
                        key={metric.label}
                        className="rounded-2xl border border-white/10 bg-[#0b0f17] p-5"
                    >
                        <div className="flex items-center justify-between">
                            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-500/10">
                                <Icon className="h-5 w-5 text-violet-400" />
                            </div>

                            <span className="text-xl font-semibold text-white">
                                {metric.value}
                            </span>
                        </div>

                        <p className="mt-4 text-sm text-white/50">
                            {metric.label}
                        </p>
                    </div>
                );
            })}
        </div>
    );
};
