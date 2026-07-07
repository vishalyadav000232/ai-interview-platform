import { CheckCircle2 } from "lucide-react";

const trustBadges = [
  "No Credit Card",
  "Free Forever Plan",
  "Cancel Anytime",
];

export default function TrustBadges() {
  return (
    <div className="mt-8 flex flex-wrap items-center justify-center gap-6 lg:justify-start">
      {trustBadges.map((item) => (
        <div
          key={item}
          className="flex items-center gap-2 text-sm font-medium text-gray-400"
        >
          <CheckCircle2 className="h-5 w-5 text-violet-500" />
          <span>{item}</span>
        </div>
      ))}
    </div>
  );
}