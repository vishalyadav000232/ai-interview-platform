import { baseAPI } from "../../../api/axios";
import type {
    ResumeUploadResponse,
    ResumeListResponse,
} from "../types/resume";

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

export const getMyResume = async (): Promise<ResumeListResponse> => {
    const response = await baseAPI.get<ResumeListResponse>(
        "/resume/my-resume",
    );

    return response.data;
};
