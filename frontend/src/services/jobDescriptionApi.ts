import api from "./api";
import type { JobAnalysis } from "../types/jobDescription";

export async function analyzeJobDescription(
    jobDescription: string
): Promise<JobAnalysis> {
    const response = await api.post<JobAnalysis>(
        "/job-description/analyze",
        {
            job_description: jobDescription,
        }
    );

    return response.data;
}