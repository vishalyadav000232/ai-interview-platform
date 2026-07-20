import { AIRecommendationCard } from "./AIRecommendationCard";
import { ATSScoreCard } from "./ATSScoreCard";
import { MetricsGrid } from "./MetricsGrid";
import { ResumeActions } from "./ResumeActions";
import { ResumeHeader } from "./ResumeHeader";
import { SkillsSection } from "./SkillsSection";

export const ResumeAnalysis = () => {
    return (
        <section className="min-h-full p-8">
            <div className="mx-auto flex max-w-7xl flex-col gap-6">

                <ResumeHeader />

                <ATSScoreCard />

                <MetricsGrid />

                <div className="grid gap-6 lg:grid-cols-2">
                    <SkillsSection />

                    <AIRecommendationCard />
                </div>

                <ResumeActions />

            </div>
        </section>
    );
};
