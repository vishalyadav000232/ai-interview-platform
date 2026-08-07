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
        },


        {
            label: "Keyword Match",
            value: `${analysis.keyword_match_percentage}%`,
            icon: Target,
        },


        {
            label: "Skills Score",
            value: `${analysis.skills_score}/30`,
            icon: Wrench,
        },


        {
            label: "Projects Score",
            value: `${analysis.projects_score}/20`,
            icon: FolderKanban,
        },


        {
            label: "Experience Score",
            value: `${analysis.experience_score}/15`,
            icon: BriefcaseBusiness,
        },


        {
            label: "ATS Status",
            value:
                analysis.overall_score >= 70
                    ? "Good"
                    : "Needs Work",
            icon: CheckCircle2,
        },

    ];





    return (

        <div className="
            grid
            gap-6
            sm:grid-cols-2
            xl:grid-cols-3
        ">


            {
                metrics.map((metric) => {


                    const Icon =
                        metric.icon;



                    return (

                        <div

                            key={
                                metric.label
                            }

                            className="
                            rounded-2xl
                            border
                            border-white/10
                            bg-[#0b0f17]
                            p-5
                            "

                        >


                            <div className="
                                flex
                                items-center
                                justify-between
                            ">


                                <div className="
                                    flex
                                    h-10
                                    w-10
                                    items-center
                                    justify-center
                                    rounded-xl
                                    bg-violet-500/10
                                ">


                                    <Icon

                                        className="
                                        h-5
                                        w-5
                                        text-violet-400
                                        "

                                    />


                                </div>




                                <span className="
                                    text-xl
                                    font-semibold
                                    text-white
                                ">

                                    {
                                        metric.value
                                    }

                                </span>


                            </div>





                            <p className="
                                mt-4
                                text-sm
                                text-white/50
                            ">

                                {
                                    metric.label
                                }


                            </p>


                        </div>


                    );

                })

            }


        </div>

    );

};
