import type { LucideIcon } from "lucide-react";

type StatCardProps = {
    icon: LucideIcon;
    iconBackground: string;
    iconColor: string;
    title: string;
    value: string;
    suffix?: string;
    description: string;
    highlight?: string;
};

export const StatCard = ({
    icon: Icon,
    iconBackground,
    iconColor,
    title,
    value,
    suffix,
    description,
    highlight,
}: StatCardProps) => {
    return (
        <div className="flex items-center gap-4 rounded-xl border border-white/10 bg-[#0b0f17] p-4">
       
            <div
                className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg"
                style={{ backgroundColor: iconBackground }}
            >
                <Icon
                    className="h-5 w-5"
                    style={{ color: iconColor }}
                    strokeWidth={2}
                />
            </div>

            <div className="flex-1">
                <p className="text-[11px] font-medium text-slate-400">
                    {title}
                </p>

                <div className="mt-1 flex items-end gap-1">
                    <span className="text-xl font-bold leading-none text-white">
                        {value}
                    </span>

                    {suffix && (
                        <span className="text-base leading-none text-slate-400">
                            {suffix}
                        </span>
                    )}
                </div>

                <p className="mt-2 text-xs leading-5 text-slate-400">
                    {highlight && (
                        <span className="mr-1 font-semibold text-green-400">
                            {highlight}
                        </span>
                    )}
                    {description}
                </p>
            </div>
        </div>
    );
};
