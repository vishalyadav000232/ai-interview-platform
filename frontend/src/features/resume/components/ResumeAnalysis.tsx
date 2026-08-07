import type { ResumeAnalysisResponse } from "../types/resume";
import { AIRecommendationCard } from "./AIRecommendationCard";
import { ATSScoreCard } from "./ATSScoreCard";
import { MetricsGrid } from "./MetricsGrid";
import { ResumeActions } from "./ResumeActions";
import { ResumeHeader } from "./ResumeHeader";
import { SkillsSection } from "./SkillsSection";


interface ResumeAnalysisProps {

    analysis: ResumeAnalysisResponse;

    resume: any;

}



export const ResumeAnalysis = ({
    analysis,
    resume,
}: ResumeAnalysisProps) => {



    console.log("this is from the resume analysi" , resume)

    return (

        <section className="
            space-y-6
        ">


            <ResumeHeader

                resume={
                    resume
                }

            />



            <ATSScoreCard

                score={
                    analysis.overall_score
                }


            />



            <MetricsGrid

                analysis={
                    analysis
                }

            />



            <div className="
                grid
                gap-6
                lg:grid-cols-2
            ">


                <SkillsSection

                    matchedSkills={
                        analysis.matched_skills
                    }


                    missingSkills={
                        analysis.missing_skills
                    }

                />



                <AIRecommendationCard

                    suggestions={
                        analysis.suggestions
                    }


                    strengths={
                        analysis.strengths
                    }


                    weaknesses={
                        analysis.weaknesses
                    }

                />


            </div>




            <ResumeActions

                resumeId={
                    resume.id
                }

            />


        </section>

    );

};
