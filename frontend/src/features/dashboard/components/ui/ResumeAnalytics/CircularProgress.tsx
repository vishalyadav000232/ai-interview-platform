type ProgressRingProps = {
    value: number;
    label: string;
    color: string;
};

export const ProgressRing = ({
    value,
    label,
    color,
}: ProgressRingProps) => {
    const radius = 38;
    const circumference = 2 * Math.PI * radius;
    const progress = circumference - (value / 100) * circumference;

    return (
        <div className="flex flex-col items-center">
            <div className="relative h-24 w-24">
                <svg
                    className="-rotate-90"
                    width="96"
                    height="96"
                    viewBox="0 0 96 96"
                >

                    <circle
                        cx="48"
                        cy="48"
                        r={radius}
                        fill="none"
                        stroke="rgba(255,255,255,0.08)"
                        strokeWidth="8"
                    />


                    <circle
                        cx="48"
                        cy="48"
                        r={radius}
                        fill="none"
                        stroke={color}
                        strokeWidth="8"
                        strokeLinecap="round"
                        strokeDasharray={circumference}
                        strokeDashoffset={progress}
                        className="transition-all duration-700"
                    />
                </svg>

                <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-lg font-semibold leading-none text-white">
                        {value}%
                    </span>
                </div>
            </div>

            <p className="mt-2 text-[11px] text-slate-400">
                {label}
            </p>
        </div>
    );
};
