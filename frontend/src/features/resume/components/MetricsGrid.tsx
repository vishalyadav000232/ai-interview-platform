import { motion } from "framer-motion";
import {
    BriefcaseBusiness,
    CheckCircle2,
    FileCheck2,
    FolderKanban,
    Target,
    Wrench,
} from "lucide-react";

interface MetricsGridProps {
    analysis: {
        resume_completeness: number;
        keyword_match_percentage: number;
        skills_score: number;
        projects_score: number;
        experience_score: number;
        overall_score: number;
    };
}

export const MetricsGrid = ({
    analysis,
}: MetricsGridProps) => {

    const metrics = [
        {
            label: "Resume Completeness",
            value: `${analysis.resume_completeness}%`,
            icon: FileCheck2,
            color: "text-sky-400",
            bg: "bg-sky-500/10",
        },
        {
            label: "Keyword Match",
            value: `${analysis.keyword_match_percentage}%`,
            icon: Target,
            color: "text-violet-400",
            bg: "bg-violet-500/10",
        },
        {
            label: "Skills Score",
            value: `${analysis.skills_score}/30`,
            icon: Wrench,
            color: "text-emerald-400",
            bg: "bg-emerald-500/10",
        },
        {
            label: "Projects Score",
            value: `${analysis.projects_score}/20`,
            icon: FolderKanban,
            color: "text-amber-400",
            bg: "bg-amber-500/10",
        },
        {
            label: "Experience Score",
            value: `${analysis.experience_score}/15`,
            icon: BriefcaseBusiness,
            color: "text-cyan-400",
            bg: "bg-cyan-500/10",
        },
        {
            label: "ATS Status",
            value:
                analysis.overall_score >= 85
                    ? "Excellent"
                    : analysis.overall_score >= 70
                        ? "Good"
                        : "Needs Work",
            icon: CheckCircle2,
            color:
                analysis.overall_score >= 70
                    ? "text-emerald-400"
                    : "text-orange-400",
            bg:
                analysis.overall_score >= 70
                    ? "bg-emerald-500/10"
                    : "bg-orange-500/10",
        },
    ];

    return (
        <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
            {metrics.map((metric, index) => {

                const Icon = metric.icon;

                return (
                    <motion.div
                        key={metric.label}
                        initial={{
                            opacity: 0,
                            y: 20,
                        }}
                        animate={{
                            opacity: 1,
                            y: 0,
                        }}
                        transition={{
                            delay: index * 0.08,
                            duration: 0.4,
                        }}
                        whileHover={{
                            y: -6,
                            scale: 1.02,
                        }}
                        className="group relative overflow-hidden rounded-3xl border border-white/10  p-6 transition-all duration-300"
                    >
                        <div className="absolute right-0 top-0 h-24 w-24 rounded-full bg-violet-500/10 blur-3xl transition-opacity duration-300 group-hover:opacity-100" />

                        <div className="relative flex items-start justify-between">

                            <div
                                className={`flex h-14 w-14 items-center justify-center rounded-2xl ${metric.bg}`}
                            >
                                <Icon
                                    className={`h-6 w-6 ${metric.color}`}
                                />
                            </div>

                            <div className="text-right">
                                <motion.h3
                                    initial={{
                                        scale: 0.9,
                                    }}
                                    animate={{
                                        scale: 1,
                                    }}
                                    transition={{
                                        delay:
                                            index * 0.08 + 0.2,
                                    }}
                                    className="text-3xl font-bold text-white"
                                >
                                    {metric.value}
                                </motion.h3>

                                <div className="mt-2 h-1.5 w-16 overflow-hidden rounded-full bg-white/10 ml-auto">
                                    <motion.div
                                        initial={{
                                            width: 0,
                                        }}
                                        animate={{
                                            width: "100%",
                                        }}
                                        transition={{
                                            delay:
                                                index * 0.08 +
                                                0.3,
                                            duration: 0.8,
                                        }}
                                        className="h-full rounded-full bg-gradient-to-r from-violet-500 to-blue-500"
                                    />
                                </div>
                            </div>

                        </div>

                        <div className="relative mt-6">

                            <p className="text-sm font-medium tracking-wide text-white/50">
                                {metric.label}
                            </p>

                        </div>
                    </motion.div>
                );
            })}
        </div>
    );
};
