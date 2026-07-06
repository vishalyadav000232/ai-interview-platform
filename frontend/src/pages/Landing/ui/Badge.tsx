import { BsStars } from "react-icons/bs";


export const Badge = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="inline-flex items-center gap-2 rounded-full border border-violet-500/40 bg-violet-500/10 px-4 py-2 text-[10px] text-violet-300">
        <BsStars />

    <span className="">
      {children}
    </span>
    </div>
  );
};