import { useState } from "react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { TabButton } from "./ui/performence/TabButton";
import { ChevronDown } from "lucide-react";

const performanceData = [
  { day: "May 12", score: 62 },
  { day: "May 13", score: 68 },
  { day: "May 14", score: 75 },
  { day: "May 15", score: 70 },
  { day: "May 16", score: 85 },
  { day: "May 17", score: 80 },
  { day: "May 18", score: 92 },
];

const tabButtons = [
  "Score",
  "Confidence",
  "Communication",
  "Technical",
];

export const PerformanceOverview = () => {
  const [activeTab, setActiveTab] = useState("Score");

  return (
    <div className="rounded-xl w-full border border-white/10 bg-[#0b0f17] p-5">

      <div className="mb-5 flex items-center justify-between">
        <h2 className="text-sm font-semibold text-white">
          Performance Overview
        </h2>

        <button
          type="button"
          className="text-xs text-slate-300 transition hover:text-white inline-flex items-center justify-center gap-1.5"
        >
          This Week
          <ChevronDown  size={18}/>
        </button>
      </div>

      <div className="mb-6 flex flex-wrap gap-2">
        {tabButtons.map((tab) => (
          <TabButton
            key={tab}
            name={tab}
            active={activeTab === tab}
            onClick={() => setActiveTab(tab)}
          />
        ))}
      </div>

      {/* Chart */}
      <div className="h-[200px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            data={performanceData}
            margin={{
              top: 15,
              right: 10,
              left: -20,
              bottom: 0,
            }}
          >
            <defs>
              <linearGradient
                id="purpleGradient"
                x1="0"
                y1="0"
                x2="0"
                y2="1"
              >
                <stop
                  offset="0%"
                  stopColor="#8B5CF6"
                  stopOpacity={0.45}
                />

                <stop
                  offset="100%"
                  stopColor="#8B5CF6"
                  stopOpacity={0}
                />
              </linearGradient>
            </defs>

            <CartesianGrid
              stroke="#1f2937"
              strokeDasharray="3 3"
              vertical={false}
            />

            <XAxis
              dataKey="day"
              axisLine={false}
              tickLine={false}
              tick={{
                fill: "#94A3B8",
                fontSize: 11,
              }}
              tickMargin={12}
            />

            <YAxis
              domain={[0, 100]}
              ticks={[0, 25, 50, 75, 100]}
              axisLine={false}
              tickLine={false}
              tick={{
                fill: "#94A3B8",
                fontSize: 11,
              }}
              tickFormatter={(value) => `${value}%`}
            />

            <Tooltip />

            <Area
              type="monotone"
              dataKey="score"
              stroke="#8B5CF6"
              strokeWidth={3}
              fill="url(#purpleGradient)"
              dot={{
                r: 4,
                fill: "#C084FC",
                stroke: "#8B5CF6",
                strokeWidth: 2,
              }}
              activeDot={{
                r: 6,
              }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
