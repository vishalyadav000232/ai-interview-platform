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
        <div className="rounded-2xl border border-white/10 bg-[#0b0f17] p-6">
            <div className="flex items-start justify-between">
                <div
                    className="flex h-12 w-12 items-center justify-center rounded-xl"
                    style={{ backgroundColor: iconBackground }}
                >
                    <Icon
                        className="h-6 w-6"
                        style={{ color: iconColor }}
                        strokeWidth={2}
                    />
                </div>
            </div>

            <div className="mt-5">
                <p className="text-sm text-slate-400">
                    {title}
                </p>

                <div className="mt-2 flex items-end gap-1">
                    <span className="text-4xl font-semibold text-white">
                        {value}
                    </span>

                    {suffix && (
                        <span className="pb-1 text-lg text-slate-400">
                            {suffix}
                        </span>
                    )}
                </div>

                <p className="mt-3 text-sm text-slate-400">
                    {highlight && (
                        <span className="font-medium text-green-400">
                            {highlight}
                        </span>
                    )}

                    {description}
                </p>
            </div>
        </div>
    );
};
