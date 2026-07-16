export interface ApiResponse<T> {

    success: boolean;

    message: string;

    data: T;

}

export interface UploadResponse {

    resume_id: string;

    original_filename: string;

    stored_filename: string;

    uploaded_at: string;

}

export interface JobDescriptionRequest {

    job_description: string;

}

export interface JobDescriptionAnalysis {

    title: string;

    experience: string;

    skills: string[];

}

export interface MatchRequest {

    resume_filename: string;

    job_description: string;

}

export interface MatchResponse {

    score: number;

    matched_skills: string[];

    missing_skills: string[];

    extra_skills: string[];

}