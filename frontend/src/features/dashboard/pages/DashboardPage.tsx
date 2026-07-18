import { AIRecommendation } from "../components/AIRecommendation";
import { HeroSection } from "../components/HeroSection";
import { MissingSkills } from "../components/MissingSkills";
import { PerformanceOverview } from "../components/PerformanceOverview";
import { RecentInterviews } from "../components/RecentInterviews";
import { ResumeAnalysis } from "../components/ResumeAnalysis";
import { SkillsProgress } from "../components/SkillsProgress";
import { StatsGrid } from "../components/StatsGrid";
import { TodayGoal } from "../components/TodayGoal";

export function DashboardPage() {
  return (
    <div className="mx-auto w-full max-w-[1600px] space-y-6">
      <HeroSection />

      <StatsGrid />

      
      <section className="grid grid-cols-1 items-stretch gap-6 xl:grid-cols-12">
        <div className="min-w-0 xl:col-span-4">
          <ResumeAnalysis />
        </div>

        <div className="min-w-0 xl:col-span-3">
          <AIRecommendation />
        </div>

        <div className="min-w-0 xl:col-span-5">
          <PerformanceOverview />
        </div>
      </section>

      <section className="grid grid-cols-1 items-stretch gap-6 xl:grid-cols-12">
        <div className="min-w-0 xl:col-span-4">
          <RecentInterviews />
        </div>

        <div className="min-w-0 xl:col-span-3">
          <SkillsProgress />
        </div>

        <div className="grid min-w-0 gap-6 xl:col-span-5">
          <MissingSkills />
          <TodayGoal />
        </div>
      </section>
    </div>
  );
}
