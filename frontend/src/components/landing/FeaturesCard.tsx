import type { LucideIcon } from "lucide-react";

type FeatureCardProps = {
  icon: LucideIcon;
  title: string;
  description: string;
  isLast?: boolean;
};

const FeatureCard = ({
  icon: Icon,
  title,
  description,
  isLast = false,
}: FeatureCardProps) => {
  return (
    <div
      className={`group relative px-6 pt-2  text-center transition-all duration-300 hover:scale-110 transition-all duration-300 ${
        !isLast ? "lg:border-r lg:border-white/10" : ""
      }`}
    >
      <Icon className="mx-auto h-10 w-10 md:h-7 md:w-7 text-violet-500 transition-transform duration-400 ease-in group-hover:scale-102" />

      <h3 className="mt-6 text-sm font-semibold text-white">
        {title}
      </h3>

      <p className="mx-auto mt-3 max-w-[230px] text-xs leading-6 text-gray-400">
        {description}
      </p>
    </div>
  );
};

export default FeatureCard;