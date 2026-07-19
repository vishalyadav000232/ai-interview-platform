import { baseAPI } from "../../../api/axios";
import type { ResumeUploadResponse } from "../types/resume";

export const uploadResume = async (
    file: File,
): Promise<ResumeUploadResponse> => {
    const formData = new FormData();

    formData.append("file", file);

    const response = await baseAPI.post<ResumeUploadResponse>(
        "/resume/upload",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        },
    );

    return response.data;
};
