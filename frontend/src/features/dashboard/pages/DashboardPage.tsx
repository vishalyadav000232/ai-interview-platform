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
    <>
      <HeroSection />

      <StatsGrid />

      <section className="grid xl:grid-cols-12 gap-6">
        <ResumeAnalysis />
        <AIRecommendation />
        <PerformanceOverview />
      </section>

      <section className="grid xl:grid-cols-12 gap-6">
        <RecentInterviews />
        <SkillsProgress />

        <div className="space-y-6">
          <MissingSkills />
          <TodayGoal />
        </div>
      </section>
    </>
  );
}
