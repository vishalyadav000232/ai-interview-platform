import { useMutation } from "@tanstack/react-query";

import { uploadResume } from "../api/resume.api";

export const useUploadResume = () => {
    return useMutation({
        mutationFn: uploadResume,
    });
};
