import { useState } from "react";
import { EmptyResumeState } from "../components/EmptyResumeState";
import { UploadResumeModal } from "../components/UploadResumeModal";

export const ResumePage = () => {
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);

    const handleResumeUpload = (file: File) => {
        console.log("Selected resume:", file);

        setIsUploadModalOpen(false);
    };

    return (
        <main className="space-y-6">
            <header>
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-violet-400">
                    Resume Intelligence
                </p>

                <h1 className="mt-2 text-2xl font-semibold tracking-tight text-white">
                    Resume Analysis
                </h1>

                <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
                    Upload your resume and get AI-powered insights to improve your
                    interview preparation.
                </p>
            </header>

            <EmptyResumeState
                onUploadClick={() => setIsUploadModalOpen(true)}
            />

            <UploadResumeModal
                open={isUploadModalOpen}
                onClose={() => setIsUploadModalOpen(false)}
                onUpload={handleResumeUpload}
            />
        </main>
    );
};
