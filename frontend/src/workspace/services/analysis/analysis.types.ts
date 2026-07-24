export interface AnalysisRequest {
    resume_id: string;
    job_description: string;
}

export interface AnalysisResponse {
    score: number;
    matched_skills: string[];
    missing_skills: string[];
    extra_skills: string[];
}