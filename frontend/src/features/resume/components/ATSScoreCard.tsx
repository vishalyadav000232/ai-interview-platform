import { motion } from "framer-motion";

interface ATSScoreCardProps {
    score: number;
}

export const ATSScoreCard = ({
    score,
}: ATSScoreCardProps) => {

    const radius = 82;
    const circumference = 2 * Math.PI * radius;

    const title =
        score >= 85
            ? "Excellent Resume"
            : score >= 70
                ? "Strong Resume"
                : score >= 50
                    ? "Good Foundation"
                    : "Needs Improvement";

    const status =
        score >= 70
            ? "ATS Friendly"
            : "Optimize Further";

    return (
        <motion.div
            initial={{
                opacity: 0,
                y: 20,
            }}
            animate={{
                opacity: 1,
                y: 0,
            }}
            transition={{
                duration: 0.45,
            }}
            className="overflow-hidden rounded-3xl border border-white/10 "
        >
            <div className="grid gap-10 p-8 lg:grid-cols-[260px_1fr]">

                <div className="flex flex-col items-center justify-center">

                    <div className="relative flex h-52 w-52 items-center justify-center">

                        <motion.div
                            animate={{
                                rotate: 360,
                            }}
                            transition={{
                                duration: 25,
                                repeat: Infinity,
                                ease: "linear",
                            }}
                            className="absolute inset-3 rounded-full border border-violet-500/10"
                        />

                        <svg
                            className="absolute inset-0 -rotate-90"
                            viewBox="0 0 200 200"
                        >
                            <circle
                                cx="100"
                                cy="100"
                                r={radius}
                                stroke="rgba(255,255,255,.08)"
                                strokeWidth="14"
                                fill="none"
                            />

                            <motion.circle
                                cx="100"
                                cy="100"
                                r={radius}
                                fill="none"
                                stroke="url(#gradient)"
                                strokeWidth="14"
                                strokeLinecap="round"
                                strokeDasharray={circumference}
                                initial={{
                                    strokeDashoffset:
                                        circumference,
                                }}
                                animate={{
                                    strokeDashoffset:
                                        circumference -
                                        (circumference *
                                            score) /
                                        100,
                                }}
                                transition={{
                                    duration: 1.6,
                                    ease: "easeOut",
                                }}
                            />

                            <defs>
                                <linearGradient
                                    id="gradient"
                                    x1="0%"
                                    y1="0%"
                                    x2="100%"
                                    y2="100%"
                                >
                                    <stop
                                        offset="0%"
                                        stopColor="#8B5CF6"
                                    />
                                    <stop
                                        offset="100%"
                                        stopColor="#3B82F6"
                                    />
                                </linearGradient>
                            </defs>
                        </svg>

                        <motion.div
                            initial={{
                                scale: 0.8,
                                opacity: 0,
                            }}
                            animate={{
                                scale: 1,
                                opacity: 1,
                            }}
                            transition={{
                                delay: 0.4,
                            }}
                            className="text-center"
                        >
                            <motion.p
                                initial={{
                                    scale: 0.7,
                                }}
                                animate={{
                                    scale: [1, 1.06, 1],
                                }}
                                transition={{
                                    duration: 1.5,
                                }}
                                className="text-6xl font-bold text-white"
                            >
                                {score}
                            </motion.p>

                            <p className="mt-1 text-sm text-white/50">
                                ATS Score
                            </p>
                        </motion.div>
                    </div>

                    <motion.div
                        initial={{
                            opacity: 0,
                            y: 12,
                        }}
                        animate={{
                            opacity: 1,
                            y: 0,
                        }}
                        transition={{
                            delay: 0.6,
                        }}
                        className="mt-6 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-4 py-2 text-sm font-medium text-emerald-400"
                    >
                        {status}
                    </motion.div>

                </div>

                <motion.div
                    initial={{
                        opacity: 0,
                        x: 20,
                    }}
                    animate={{
                        opacity: 1,
                        x: 0,
                    }}
                    transition={{
                        delay: 0.2,
                    }}
                >
                    <div className="flex items-center gap-3">

                        <motion.div
                            whileHover={{
                                scale: 1.08,
                                rotate: 8,
                            }}
                            className="flex h-12 w-12 items-center justify-center rounded-2xl bg-violet-500/10"
                        >
                            <svg
                                width="24"
                                height="24"
                                viewBox="0 0 24 24"
                                fill="none"
                            >
                                <path
                                    d="M12 2L14.8 8.2L21.5 9L16.5 13.5L17.8 20L12 16.7L6.2 20L7.5 13.5L2.5 9L9.2 8.2L12 2Z"
                                    stroke="#A78BFA"
                                    strokeWidth="1.8"
                                />
                            </svg>
                        </motion.div>

                        <div>

                            <p className="text-sm text-violet-400">
                                ATS Compatibility
                            </p>

                            <h2 className="text-3xl font-bold text-white">
                                {title}
                            </h2>

                        </div>

                    </div>

                    <p className="mt-6 max-w-2xl text-base leading-7 text-white/60">
                        Your resume has a solid foundation for ATS screening.
                        Improving missing keywords, measurable achievements,
                        and formatting will further increase your interview
                        chances.
                    </p>

                    <div className="mt-8 grid gap-4 md:grid-cols-3">

                        {[
                            {
                                label: "Ranking",
                                value: `Top ${Math.max(
                                    1,
                                    100 - score
                                )}%`,
                            },
                            {
                                label: "Recruiter View",
                                value:
                                    score >= 70
                                        ? "Positive"
                                        : "Average",
                            },
                            {
                                label: "Recommendation",
                                value:
                                    score >= 70
                                        ? "Ready"
                                        : "Optimize",
                            },
                        ].map(
                            (
                                item,
                                index,
                            ) => (
                                <motion.div
                                    key={item.label}
                                    initial={{
                                        opacity: 0,
                                        y: 20,
                                    }}
                                    animate={{
                                        opacity: 1,
                                        y: 0,
                                    }}
                                    transition={{
                                        delay:
                                            0.5 +
                                            index *
                                            0.15,
                                    }}
                                    whileHover={{
                                        y: -6,
                                        scale: 1.03,
                                    }}
                                    className="rounded-2xl border border-white/10 bg-white/[0.03] p-4 transition"
                                >
                                    <p className="text-xs uppercase tracking-wider text-white/40">
                                        {item.label}
                                    </p>

                                    <p className="mt-2 text-xl font-semibold text-white">
                                        {item.value}
                                    </p>
                                </motion.div>
                            )
                        )}

                    </div>

                </motion.div>

            </div>
        </motion.div>
    );
};
