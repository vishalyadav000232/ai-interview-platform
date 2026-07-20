export type ResumeStatus =
    | "uploaded"
    | "queued"
    | "processing"
    | "analyzed"
    | "failed";

export interface ResumeData {
    id: string;
    file_name: string;
    original_file_name: string;
    file_size: number;
    status: ResumeStatus;
    created_at: string;
    updated_at: string;
}

export interface ResumeUploadResponse {
    success: boolean;
    message: string;
    data: ResumeData;
}

export interface ResumeListResponse {
    success: boolean;
    message: string;
    data: ResumeData[];
}
