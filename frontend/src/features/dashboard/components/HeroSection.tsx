import { RecommendationCard } from "./ui/hero/RecommendationCard";
import { StreakCard } from "./ui/hero/StreakCard";


export const HeroSection = () => {
    return (
        <section className="grid gap-6 xl:grid-cols-12">
            <div className="xl:col-span-8">
                <RecommendationCard />
            </div>

            <div className="xl:col-span-4">
                <StreakCard />
            </div>
        </section>
    );
};

