export interface AnalysisRequest {
    resume_id: string;
    job_description: string;
}

export interface AnalysisResponse {
    score: number;
    role_id: string;
    matched_skills: string[];
    missing_skills: string[];
    matched_technologies: string[];
    missing_technologies: string[];
    extra_skills: string[];
}