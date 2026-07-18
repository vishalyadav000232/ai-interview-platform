type TabButtonProps = {
    name: string;
    active?: boolean;
    onClick?: () => void;
};

export const TabButton = ({
    name,
    active = false,
    onClick,
}: TabButtonProps) => {
    return (
        <button
            onClick={onClick}
            className={`rounded-lg px-2 py-1 text-[11px] font-medium transition-all duration-200 ${active
                    ? "bg-violet-600 text-white"
                    : "border border-white/10 bg-transparent text-slate-300 hover:bg-white/5 hover:text-white"
                }`}
        >
            {name}
        </button>
    );
};
