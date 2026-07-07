import React from "react";
import {
  FileUp,
  Bot,
  Mic,
  ChartNoAxesColumnIncreasing,
} from "lucide-react";

import StepCard from "../../../components/landing/StepCard";
import { Connector } from "../../../components/landing/Conecter";


const steps = [
  {
    step: "1",
    icon: FileUp,
    title: "Upload Resume",
    description:
      "Upload your resume and let AI analyze your profile instantly.",
  },
  {
    step: "2",
    icon: Bot,
    title: "Choose Interview",
    description:
      "Select your company, role and interview difficulty.",
  },
  {
    step: "3",
    icon: Mic,
    title: "Practice with AI",
    description:
      "Answer realistic interview questions in voice or text.",
  },
  {
    step: "4",
    icon: ChartNoAxesColumnIncreasing,
    title: "Get Feedback",
    description:
      "Receive detailed AI feedback, ATS score and improvement tips.",
  },
];

const HowItWorks = () => {
  return (
    <section className="bg-[#000204] py-24 text-white">
      <div className=" relative mx-auto max-w-7xl px-5">

        <div className="absolute -left-24 top-10 -z-0 h-[420px] w-[420px] rounded-full bg-violet-600/20 blur-[140px]" />

        <div className="absolute right-24 -top-10 -z-0 h-[420px] w-[420px] rounded-full bg-violet-600/20 blur-[140px]" />
      
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="text-3xl font-bold sm:text-4xl lg:text-5xl">
            How It{" "}
            <span className="bg-gradient-to-r from-violet-500 to-fuchsia-500 bg-clip-text text-transparent">
              Works
            </span>
          </h2>

          <p className="mt-5 text-sm text-gray-400 sm:text-base">
            Prepare for your dream interview in just four simple AI-powered
            steps.
          </p>
        </div>

      
        <div className="mt-16 flex flex-col gap-10 lg:flex-row lg:items-center lg:justify-between">
          {steps.map((step, index) => (
            <React.Fragment key={step.step}>
              <StepCard {...step}  />

              {index !== steps.length - 1 && <Connector />}
            </React.Fragment>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;