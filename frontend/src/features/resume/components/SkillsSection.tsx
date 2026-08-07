import { CheckCircle2, CircleAlert } from "lucide-react";


interface SkillsSectionProps {
    matchedSkills: string[];
    missingSkills: string[];
}


export const SkillsSection = ({
    matchedSkills,
    missingSkills,
}: SkillsSectionProps) => {


    return (
        <div className="rounded-2xl border border-white/10 bg-[#0b0f17] p-6">


            <h2 className="text-lg font-semibold text-white">
                Skills Analysis
            </h2>



            {/* Matched Skills */}

            <div className="mt-6">

                <div className="flex items-center gap-2">

                    <CheckCircle2 className="h-5 w-5 text-green-400" />


                    <h3 className="font-medium text-green-400">
                        Matched Skills
                    </h3>

                </div>



                <div className="mt-4 flex flex-wrap gap-3">


                    {
                        matchedSkills?.map((skill) => (

                            <span
                                key={skill}
                                className="
                                rounded-full
                                border
                                border-green-500/20
                                bg-green-500/10
                                px-3
                                py-1
                                text-sm
                                text-green-400
                                "
                            >

                                {skill}

                            </span>

                        ))
                    }


                </div>

            </div>





            {/* Missing Skills */}

            <div className="mt-8">


                <div className="flex items-center gap-2">

                    <CircleAlert className="h-5 w-5 text-amber-400" />


                    <h3 className="font-medium text-amber-400">
                        Missing Skills
                    </h3>


                </div>



                <div className="mt-4 flex flex-wrap gap-3">


                    {
                        missingSkills?.map((skill) => (

                            <span
                                key={skill}
                                className="
                                rounded-full
                                border
                                border-amber-500/20
                                bg-amber-500/10
                                px-3
                                py-1
                                text-sm
                                text-amber-400
                                "
                            >

                                {skill}

                            </span>

                        ))
                    }


                </div>


            </div>


        </div>
    );
};
