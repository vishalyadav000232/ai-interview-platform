import { baseAPI } from "../../../api/axios";
import type {
    ResumeUploadResponse,
    ResumeListResponse,
    ResumeAnalysisResponse
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


export const getResumeAnalysis = async (
    resumeId: string,
): Promise<ResumeAnalysisResponse> => {


    const response = await baseAPI.get<ResumeAnalysisResponse>(
        `/resume/${resumeId}/analysis`
    );




    return response.data;

};



export const downloadResume = async (
    resumeId: string,
) => {

    const response = await baseAPI.get(
        `/resume/download/${resumeId}`,
        {
            responseType: "blob",
        },
    );

    return response.data;

};
