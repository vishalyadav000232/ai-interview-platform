export type ResumeStatus =
    | "uploaded"
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
    message: string;
    data: ResumeData;
}
