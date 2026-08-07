import { motion } from "framer-motion";
import {
    Calendar,
    Download,
    FileText,
    Sparkles,
} from "lucide-react";

interface ResumeHeaderProps {
    resume: any;
    onDownloadResume: () => void;
}

export const ResumeHeader = ({
    resume,
    onDownloadResume,
}: ResumeHeaderProps) => {

    const uploadedDate = resume?.created_at
        ? new Date(
            resume.created_at
        ).toLocaleDateString(
            "en-US",
            {
                day: "numeric",
                month: "short",
                year: "numeric",
            }
        )
        : "Today";


    return (

        <motion.div

            initial={{
                opacity: 0,
                y: -20,
            }}

            whileInView={{
                opacity: 1,
                y: 0,
            }}

            viewport={{
                once: true,
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
                p-7
            "
        >


            <div className="
                absolute
                -right-10
                -top-10
                h-44
                w-44
                rounded-full
                bg-violet-500/10
                blur-3xl
            " />


            <div className="
                absolute
                -left-8
                bottom-0
                h-32
                w-32
                rounded-full
                bg-blue-500/10
                blur-3xl
            " />



            <div className="
                relative
                flex
                flex-col
                gap-6
                lg:flex-row
                lg:items-center
                lg:justify-between
            ">



                <div className="
                    flex
                    items-start
                    gap-5
                ">



                    <motion.div

                        initial={{
                            scale: 0,
                            rotate: -20,
                        }}

                        whileInView={{
                            scale: 1,
                            rotate: 0,
                        }}

                        viewport={{
                            once: true,
                        }}

                        transition={{
                            type: "spring",
                            stiffness: 180,
                            damping: 12,
                        }}

                        className="
                            flex
                            h-16
                            w-16
                            items-center
                            justify-center
                            rounded-2xl
                            bg-violet-500/10
                        "
                    >

                        <FileText
                            className="
                                h-8
                                w-8
                                text-violet-400
                            "
                        />

                    </motion.div>




                    <div>


                        <div className="
                            flex
                            items-center
                            gap-2
                        ">


                            <h1 className="
                                text-3xl
                                font-bold
                                tracking-tight
                                text-white
                            ">

                                Resume Analysis

                            </h1>


                            <Sparkles
                                className="
                                    h-5
                                    w-5
                                    text-violet-400
                                "
                            />


                        </div>





                        <p className="
                            mt-2
                            max-w-2xl
                            text-sm
                            leading-6
                            text-white/50
                        ">

                            AI analyzed your resume and generated an ATS
                            compatibility report with strengths, weaknesses,
                            and personalized recommendations.

                        </p>





                        <div className="
                            mt-5
                            flex
                            flex-wrap
                            items-center
                            gap-3
                        ">



                            <div className="
                                flex
                                items-center
                                gap-2
                                rounded-xl
                                border
                                border-white/10
                                bg-white/5
                                px-3
                                py-2
                                text-sm
                                text-white/70
                            ">


                                <FileText
                                    className="
                                        h-4
                                        w-4
                                        text-violet-400
                                    "
                                />


                                <span className="
                                    max-w-[220px]
                                    truncate
                                ">

                                    {
                                        resume?.original_file_name ??
                                        "Resume.pdf"
                                    }

                                </span>


                            </div>






                            <div className="
                                rounded-full
                                border
                                border-emerald-500/20
                                bg-emerald-500/10
                                px-3
                                py-1
                                text-xs
                                font-semibold
                                uppercase
                                tracking-wide
                                text-emerald-400
                            ">


                                {
                                    resume?.status ??
                                    "Analyzed"
                                }


                            </div>






                            <div className="
                                flex
                                items-center
                                gap-2
                                rounded-xl
                                border
                                border-white/10
                                bg-white/5
                                px-3
                                py-2
                                text-sm
                                text-white/70
                            ">


                                <Calendar
                                    className="
                                        h-4
                                        w-4
                                        text-sky-400
                                    "
                                />

                                {uploadedDate}


                            </div>



                        </div>


                    </div>



                </div>







                <motion.button

                    type="button"

                    onClick={
                        onDownloadResume
                    }

                    whileHover={{
                        scale: 1.03,
                    }}

                    whileTap={{
                        scale: 0.97,
                    }}

                    disabled={
                        !resume?.id
                    }

                    className="
                        inline-flex
                        items-center
                        justify-center
                        gap-2
                        rounded-xl
                        border
                        border-white/10
                        bg-white/5
                        px-5
                        py-3
                        text-sm
                        font-medium
                        text-white
                        backdrop-blur-sm
                        transition
                        hover:bg-white/10
                        disabled:cursor-not-allowed
                        disabled:opacity-50
                    "
                >

                    <Download
                        className="
                            h-4
                            w-4
                            text-violet-400
                        "
                    />

                    Download Resume


                </motion.button>



            </div>



        </motion.div>

    );
};
