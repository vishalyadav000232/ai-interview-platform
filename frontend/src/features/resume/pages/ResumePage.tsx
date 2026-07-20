import { useState } from "react";

import { EmptyResumeState } from "../components/EmptyResumeState";
import { ProcessingResumeState } from "../components/ProcessingResumeState";
import { ResumeAnalysis } from "../components/ResumeAnalysis";
import { UploadResumeModal } from "../components/UploadResumeModal";

import { useMyResume } from "../hooks/useMyResume";
import { useUploadResume } from "../hooks/useUpload";

export const ResumePage = () => {
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);

    const uploadResumeMutation = useUploadResume();

    const {
        data,
        isLoading,
        isError,
        error,
    } = useMyResume();

    const latestResume = data?.data?.[0];

    const resumeStatus = latestResume?.status?.toLowerCase();

    const handleResumeUpload = (file: File) => {
        uploadResumeMutation.mutate(file, {
            onSuccess: (response) => {
                console.log("Resume uploaded:", response);
                setIsUploadModalOpen(false);
            },

            onError: (uploadError) => {
                console.error(
                    "Resume upload failed:",
                    uploadError,
                );
            },
        });
    };

    if (isLoading) {
        return (
            <section className="flex min-h-full items-center justify-center p-8 text-white">
                <p className="text-sm text-white/50">
                    Loading your resume...
                </p>
            </section>
        );
    }

    if (isError) {
        console.error("Failed to fetch resumes:", error);

        return (
            <section className="flex min-h-full items-center justify-center p-8 text-white">
                <div className="rounded-xl border border-red-500/20 bg-red-500/10 p-5 text-center">
                    <h2 className="font-semibold text-red-400">
                        Unable to load resume
                    </h2>

                    <p className="mt-2 text-sm text-white/50">
                        Please refresh the page and try again.
                    </p>
                </div>
            </section>
        );
    }

    if (
        resumeStatus === "uploaded" ||
        resumeStatus === "queued" ||
        resumeStatus === "processing"
    ) {
        return <ProcessingResumeState />;
    }

    if (resumeStatus === "analyzed") {
        return <ResumeAnalysis />;
    }

    if (resumeStatus === "failed") {
        return (
            <section className="min-h-full p-8 text-white">
                <div className="mx-auto max-w-3xl rounded-2xl border border-red-500/20 bg-[#0b0f17] p-6">
                    <h1 className="text-xl font-semibold text-red-400">
                        Resume analysis failed
                    </h1>

                    <p className="mt-2 text-sm text-white/50">
                        Something went wrong while processing your
                        resume. Please upload it again.
                    </p>

                    {latestResume?.failure_reason && (
                        <p className="mt-4 rounded-xl bg-red-500/10 p-4 text-sm text-red-300">
                            {latestResume.failure_reason}
                        </p>
                    )}

                    <button
                        type="button"
                        onClick={() => setIsUploadModalOpen(true)}
                        className="mt-6 rounded-xl bg-violet-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-violet-500"
                    >
                        Upload Resume Again
                    </button>

                    <UploadResumeModal
                        open={isUploadModalOpen}
                        onClose={() =>
                            setIsUploadModalOpen(false)
                        }
                        onUpload={handleResumeUpload}
                        isUploading={
                            uploadResumeMutation.isPending
                        }
                    />
                </div>
            </section>
        );
    }

    return (
        <>
            <EmptyResumeState
                onUploadClick={() =>
                    setIsUploadModalOpen(true)
                }
            />

            <UploadResumeModal
                open={isUploadModalOpen}
                onClose={() =>
                    setIsUploadModalOpen(false)
                }
                onUpload={handleResumeUpload}
                isUploading={
                    uploadResumeMutation.isPending
                }
            />
        </>
    );
};
