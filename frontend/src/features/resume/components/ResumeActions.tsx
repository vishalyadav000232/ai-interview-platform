import { motion } from "framer-motion";
import {
    ArrowRight,
    Download,
    RefreshCcw,
    Sparkles,
    Rocket,
} from "lucide-react";

interface ResumeActionsProps {
    onReplaceResume?: () => void;
    onStartInterview?: () => void;
    onDownloadResume?: () => void;
}

export const ResumeActions = ({
    onReplaceResume,
    onStartInterview,
    onDownloadResume,
}: ResumeActionsProps) => {

    const buttonAnimation = {
        whileHover: {
            scale: 1.04,
            y: -5,
        },
        whileTap: {
            scale: 0.97,
        },
    };


    return (

        <motion.div

            initial={{
                opacity: 0,
                y: 30,
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
                duration: 0.5,
            }}

            className="
                relative
                overflow-hidden
                rounded-3xl
                border
                border-white/10
                bg-[#0b0f17]
                p-8
            "
        >

            <div className="
                absolute
                -right-20
                -top-20
                h-64
                w-64
                rounded-full
                bg-violet-500/10
                blur-3xl
            " />


            <div className="
                absolute
                -bottom-24
                -left-16
                h-52
                w-52
                rounded-full
                bg-blue-500/10
                blur-3xl
            " />


            <div className="relative">


                <div className="
                    flex
                    items-center
                    justify-between
                    gap-5
                ">

                    <div className="
                        flex
                        items-center
                        gap-4
                    ">


                        <div className="
                            flex
                            h-14
                            w-14
                            items-center
                            justify-center
                            rounded-2xl
                            border
                            border-violet-500/20
                            bg-violet-500/10
                        ">

                            <Sparkles className="
                                h-7
                                w-7
                                text-violet-400
                            " />

                        </div>



                        <div>

                            <h2 className="
                                text-2xl
                                font-bold
                                text-white
                            ">

                                Ready for Your Next Step?

                            </h2>


                            <p className="
                                mt-1
                                text-sm
                                text-white/50
                            ">

                                Continue your career preparation journey with AI-powered tools.

                            </p>

                        </div>


                    </div>



                    <Rocket className="
                        hidden
                        h-8
                        w-8
                        text-violet-400/60
                        md:block
                    " />


                </div>





                <div className="
                    mt-8
                    grid
                    gap-5
                    md:grid-cols-3
                ">



                    <motion.button

                        {...buttonAnimation}

                        onClick={onStartInterview}

                        className="
                            group
                            relative
                            overflow-hidden
                            flex
                            items-center
                            justify-center
                            gap-3
                            rounded-2xl
                            bg-gradient-to-r
                            from-violet-600
                            to-indigo-600
                            px-6
                            py-4
                            font-semibold
                            text-white
                            shadow-xl
                            shadow-violet-900/30
                        "
                    >

                        <div className="
                            absolute
                            inset-0
                            translate-y-full
                            bg-white/10
                            transition
                            duration-300
                            group-hover:translate-y-0
                        " />


                        <ArrowRight className="
                            relative
                            h-5
                            w-5
                            transition-transform
                            group-hover:translate-x-1
                        " />


                        <span className="relative">
                            Start AI Interview
                        </span>


                    </motion.button>







                    <motion.button

                        {...buttonAnimation}

                        onClick={onReplaceResume}

                        className="
                            group
                            flex
                            items-center
                            justify-center
                            gap-3
                            rounded-2xl
                            border
                            border-white/10
                            bg-white/[0.04]
                            px-6
                            py-4
                            font-semibold
                            text-white
                            backdrop-blur-sm
                            transition
                            hover:border-orange-400/30
                            hover:bg-orange-500/10
                        "
                    >

                        <RefreshCcw className="
                            h-5
                            w-5
                            text-orange-400
                            transition-transform
                            group-hover:rotate-180
                        " />


                        Replace Resume


                    </motion.button>








                    <motion.button

                        {...buttonAnimation}

                        onClick={onDownloadResume}

                        className="
                            group
                            flex
                            items-center
                            justify-center
                            gap-3
                            rounded-2xl
                            border
                            border-white/10
                            bg-white/[0.04]
                            px-6
                            py-4
                            font-semibold
                            text-white
                            backdrop-blur-sm
                            transition
                            hover:border-emerald-400/30
                            hover:bg-emerald-500/10
                        "
                    >

                        <Download className="
                            h-5
                            w-5
                            text-emerald-400
                            transition-transform
                            group-hover:-translate-y-1
                        " />


                        Download Resume


                    </motion.button>



                </div>



            </div>


        </motion.div>

    );
};
