
export const StatsGrid = () => {
  return (
    <section className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">
      {/* Stat Card 1 */}
      <div className="rounded-xl border border-white/10 bg-[#0b0f17] p-5">
        Resume Score
      </div>

      {/* Stat Card 2 */}
      <div className="rounded-xl border border-white/10 bg-[#0b0f17] p-5">
        Interviews
      </div>

      {/* Stat Card 3 */}
      <div className="rounded-xl border border-white/10 bg-[#0b0f17] p-5">
        Success Rate
      </div>

      {/* Stat Card 4 */}
      <div className="rounded-xl border border-white/10 bg-[#0b0f17] p-5">
        Practice Time
      </div>
    </section>
  );
};
