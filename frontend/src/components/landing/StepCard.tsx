import type { LucideIcon } from "lucide-react";
type StepCardProps = {
  step: string;
  icon: LucideIcon;
  title: string;
  description: string;
};

const StepCard = ({
  step ,
  icon: Icon,
  title,
  description,
}: StepCardProps) => {
  return (
    <div className="group flex items-center gap-5">
      <div className="flex shrink-0 h-20 w-20 items-center justify-center rounded-full border md:h-15 md:w-15 bg-violet-500/10 backdrop:backdrop-blur-lg">
        <Icon className="h-8 w-8 text-violet-500 transition-transform duration-300 group-hover:scale-105 md:h-5 md:w-5" />
      </div>

      <div className="flex flex-col gap-1">
        <h3 className="text-[12px] font-semibold ">
          {step}. {title}
        </h3>

        <p className="text-[10px] text-gray-200/70">
          {description}
        </p>
      </div>
    </div>
  );
};

export default StepCard;