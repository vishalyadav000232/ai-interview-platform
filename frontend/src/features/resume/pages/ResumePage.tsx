import { useState } from "react";

import { EmptyResumeState } from "../components/EmptyResumeState";
import { ProcessingResumeState } from "../components/ProcessingResumeState";
import { UploadResumeModal } from "../components/UploadResumeModal";

import { useUploadResume } from "../hooks/useUpload";
import { useMyResume } from "../hooks/useMyResume";


export const ResumePage = () => {
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);

    const uploadResumeMutation = useUploadResume();

    const { data, isLoading } = useMyResume();

    const latestResume = data?.data?.[0];
    console.log("this is the latest reusne" , latestResume)

    const handleResumeUpload = (file: File) => {
        uploadResumeMutation.mutate(file, {
            onSuccess: () => {
                setIsUploadModalOpen(false);
            },

            onError: (error) => {
                console.error("Resume upload failed:", error);
            },
        });
    };

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (
        latestResume?.status === "queued" ||
        latestResume?.status === "processing"
    ) {
        return <ProcessingResumeState />;
    }

    return (
        <>
            <EmptyResumeState
                onUploadClick={() => setIsUploadModalOpen(true)}
            />

            <UploadResumeModal
                open={isUploadModalOpen}
                onClose={() => setIsUploadModalOpen(false)}
                onUpload={handleResumeUpload}
                isUploading={uploadResumeMutation.isPending}
            />
        </>
    );
};
