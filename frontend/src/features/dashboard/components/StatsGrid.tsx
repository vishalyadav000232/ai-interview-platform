import {
  FileText,
  Flame,
  Video,
  ChartColumn,
} from "lucide-react";
import { StatCard } from "./ui/stats/StatCard";



export const StatsGrid = () => {
  return (
    <section className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
      <StatCard
        icon={FileText}
        iconBackground="#0f2e22"
        iconColor="#22c55e"
        title="Resume Score"
        value="78"
        suffix="/100"
        highlight="+8 "
        description="points from last analysis"
      />

      <StatCard
        icon={ChartColumn}
        iconBackground="#2b1946"
        iconColor="#a855f7"
        title="Overall Interview Score"
        value="82"
        suffix="%"
        highlight="+12% "
        description="from last 7 days"
      />

      <StatCard
        icon={Video}
        iconBackground="#102847"
        iconColor="#3b82f6"
        title="Mock Interviews"
        value="12"
        description="Total Completed"
      />

      <StatCard
        icon={Flame}
        iconBackground="#3a2212"
        iconColor="#fb923c"
        title="Current Streak"
        value="7"
        suffix="Days"
        highlight="Keep it alive! "
        description=""
      />
    </section>
  );
};
