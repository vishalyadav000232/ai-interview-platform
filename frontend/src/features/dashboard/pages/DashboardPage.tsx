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
    <div className="space-y-2">
      <HeroSection />

      <StatsGrid />


      <section className="grid grid-cols-1 xl:grid-cols-12 gap-6">
        <div className="xl:col-span-5">
          <ResumeAnalysis />
        </div>

        <div className="xl:col-span-7 space-y-6 bg-amber-300">
          <AIRecommendation />
          <PerformanceOverview />
        </div>
      </section>

      {/* Row 2 */}
      <section className="grid grid-cols-1 xl:grid-cols-12 gap-6">
        <div className="xl:col-span-8">
          <RecentInterviews />
        </div>

        <div className="xl:col-span-4 space-y-6">
          <SkillsProgress />
          <MissingSkills />
          <TodayGoal />
        </div>
      </section>
    </div>
  );
}
