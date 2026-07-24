import api from "../api/client";

export interface OptimizeResponse {
    success: boolean;
    message: string;
    data: {
        optimized_filename: string;
        blocks: any[];
        layout: any;
    };
}

export const optimizeResume = async (
    resumeFilename: string,
    jobDescription: string,
    selectedSkills: string[]
): Promise<OptimizeResponse> => {

    const response = await api.post(
        "/optimization/optimize",
        {
            resume_filename: resumeFilename,
            job_description: jobDescription,
            selected_skills: selectedSkills,
        }
    );

    return response.data;
};