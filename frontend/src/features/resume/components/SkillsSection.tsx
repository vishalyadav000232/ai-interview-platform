import { motion } from "framer-motion";
import {
    CheckCircle2,
    CircleAlert,
    Sparkles,
} from "lucide-react";

interface SkillsSectionProps {
    matchedSkills: string[];
    missingSkills: string[];
}

export const SkillsSection = ({
    matchedSkills,
    missingSkills,
}: SkillsSectionProps) => {
    return (
        <motion.div
            initial={{
                opacity: 0,
                y: 40,
            }}
            whileInView={{
                opacity: 1,
                y: 0,
            }}
            viewport={{
                once: true,
                amount: 0.25,
            }}
            transition={{
                duration: 0.6,
                ease: "easeOut",
            }}
            className="relative overflow-hidden rounded-3xl border border-white/10  p-7"
        >
            <div className="absolute -right-10 top-0 h-40 w-40 rounded-full bg-violet-600/10 blur-3xl" />
            <div className="absolute -left-10 bottom-0 h-32 w-32 rounded-full bg-emerald-500/10 blur-3xl" />

            <div className="relative">
                <div className="flex items-center justify-between">
                    <div>
                        <h2 className="text-xl font-bold text-white">
                            Skills Analysis
                        </h2>

                        <p className="mt-1 text-sm text-white/50">
                            AI matched your resume against essential backend
                            technologies.
                        </p>
                    </div>

                    <motion.div
                        initial={{
                            scale: 0,
                            rotate: -180,
                        }}
                        whileInView={{
                            scale: 1,
                            rotate: 0,
                        }}
                        viewport={{
                            once: true,
                        }}
                        transition={{
                            duration: 0.6,
                            delay: 0.2,
                            type: "spring",
                        }}
                        className="flex h-12 w-12 items-center justify-center rounded-2xl bg-violet-500/10"
                    >
                        <Sparkles className="h-6 w-6 text-violet-400" />
                    </motion.div>
                </div>

                <motion.div
                    initial={{
                        opacity: 0,
                        y: 25,
                    }}
                    whileInView={{
                        opacity: 1,
                        y: 0,
                    }}
                    viewport={{
                        once: true,
                        amount: 0.2,
                    }}
                    transition={{
                        delay: 0.2,
                    }}
                    className="mt-8"
                >
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <CheckCircle2 className="h-5 w-5 text-emerald-400" />

                            <h3 className="font-semibold text-emerald-400">
                                Matched Skills
                            </h3>
                        </div>

                        <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-400">
                            {matchedSkills.length} Skills
                        </span>
                    </div>

                    <div className="mt-5 flex flex-wrap gap-3">
                        {matchedSkills.map((skill, index) => (
                            <motion.div
                                key={skill}
                                initial={{
                                    opacity: 0,
                                    scale: 0.8,
                                    y: 20,
                                }}
                                whileInView={{
                                    opacity: 1,
                                    scale: 1,
                                    y: 0,
                                }}
                                viewport={{
                                    once: true,
                                    amount: 0.2,
                                }}
                                transition={{
                                    duration: 0.35,
                                    delay: index * 0.06,
                                }}
                                whileHover={{
                                    scale: 1.08,
                                    y: -3,
                                }}
                                whileTap={{
                                    scale: 0.95,
                                }}
                                className="rounded-2xl border border-emerald-500/20 bg-emerald-500/10 px-4 py-2 text-sm font-medium text-emerald-300"
                            >
                                {skill}
                            </motion.div>
                        ))}
                    </div>
                </motion.div>

                <motion.div
                    initial={{
                        opacity: 0,
                        y: 25,
                    }}
                    whileInView={{
                        opacity: 1,
                        y: 0,
                    }}
                    viewport={{
                        once: true,
                        amount: 0.2,
                    }}
                    transition={{
                        delay: 0.35,
                    }}
                    className="mt-10"
                >
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <CircleAlert className="h-5 w-5 text-orange-400" />

                            <h3 className="font-semibold text-orange-400">
                                Missing Skills
                            </h3>
                        </div>

                        <span className="rounded-full bg-orange-500/10 px-3 py-1 text-xs font-medium text-orange-400">
                            {missingSkills.length} Missing
                        </span>
                    </div>

                    <div className="mt-5 flex flex-wrap gap-3">
                        {missingSkills.map((skill, index) => (
                            <motion.div
                                key={skill}
                                initial={{
                                    opacity: 0,
                                    scale: 0.8,
                                    y: 20,
                                }}
                                whileInView={{
                                    opacity: 1,
                                    scale: 1,
                                    y: 0,
                                }}
                                viewport={{
                                    once: true,
                                    amount: 0.2,
                                }}
                                transition={{
                                    duration: 0.35,
                                    delay: 0.2 + index * 0.06,
                                }}
                                whileHover={{
                                    scale: 1.08,
                                    y: -3,
                                }}
                                whileTap={{
                                    scale: 0.95,
                                }}
                                className="rounded-2xl border border-orange-500/20 bg-orange-500/10 px-4 py-2 text-sm font-medium text-orange-300"
                            >
                                {skill}
                            </motion.div>
                        ))}
                    </div>
                </motion.div>
            </div>
        </motion.div>
    );
};
