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
    failure_reason: string;

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





export interface ResumeAnalysisResponse {
    id: string;
    resume_id: string;

    overall_score: number;

    profile_score: number;
    skills_score: number;
    education_score: number;
    experience_score: number;
    projects_score: number;

    resume_completeness: number;
    keyword_match_percentage: number;

    matched_skills: string[];
    missing_skills: string[];

    suggestions: string[];
    strengths: string[];
    weaknesses: string[];

    analysis_version: string;
    analysis_time_ms: number;

    created_at: string;
    updated_at: string;
}
