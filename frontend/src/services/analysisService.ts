import axios from "axios";

import type {
    ApiResponse,
    UploadResponse,
    JobDescriptionAnalysis,
    MatchResponse,
} from "../types/analysis";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
});

export async function uploadResume(
    file: File
): Promise<UploadResponse> {

    const formData = new FormData();

    formData.append("file", file);

    const response =
        await api.post<ApiResponse<UploadResponse>>(
            "/resume/upload",
            formData,
            {
                headers: {
                    "Content-Type":
                        "multipart/form-data",
                },
            }
        );

    return response.data.data;

}

export async function analyzeJobDescription(
    jobDescription: string
): Promise<JobDescriptionAnalysis> {

    const response =
        await api.post<JobDescriptionAnalysis>(
            "/job-description/analyze",
            {
                job_description: jobDescription,
            }
        );

    return response.data;

}

export async function matchResume(
    resumeId: string,
    jobDescription: string
): Promise<MatchResponse> {

    const response =
        await api.post<MatchResponse>(
            "/analysis/match",
            {
                resume_id: resumeId,
                job_description: jobDescription,
            }
        );

    return response.data;

}