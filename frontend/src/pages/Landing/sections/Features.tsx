import {
  Bot,
  FileText,
  Sparkles,
  ChartNoAxesColumnIncreasing,
  CircleHelp,
  Building2,
} from "lucide-react";
import FeatureCard from "../../../components/landing/FeaturesCard";

const features = [
  {
    icon: Bot,
    title: "AI Mock Interviews",
    description: "Realistic AI interviews tailored to your target role",
  },
  {
    icon: FileText,
    title: "Resume Analysis",
    description: "Get ATS score, keyword insights and improvement tips",
  },
  {
    icon: Sparkles,
    title: "Smart Feedback",
    description: "AI-powered feedback to improve your answers and confidence",
  },
  {
    icon: ChartNoAxesColumnIncreasing,
    title: "Track Progress",
    description: "Detailed analytics to track your improvement over time",
  },
  {
    icon: CircleHelp,
    title: "Practice Questions",
    description: "Role-specific questions with detailed explanations",
  },
  {
    icon: Building2,
    title: "Company Insights",
    description: "Interview process insights from top companies",
  },
];

function Features() {
  return (
    <section className="relative bg-[#000204] px-5 py-20 text-white">
  <div className="relative mx-auto max-w-7xl">

    <div className="absolute -left-24 top-10 -z-10 h-[420px] w-[420px] rounded-full bg-violet-600/20 blur-[140px]" />

    <div className="grid overflow-hidden rounded-2xl border border-white/10 shadow-2xl shadow-violet-500/5 bg-amber-200 md:grid-cols-2 lg:grid-cols-6 py-7 gap-4">

      {features.map((feature, index) => (
  <FeatureCard
    key={feature.title}
    {...feature}
    isLast={index === features.length - 1}
  />
))}

    </div>

  </div>
</section>
  );
}

export default Features;