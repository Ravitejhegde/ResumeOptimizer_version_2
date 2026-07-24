import api from "../api/client";

export interface OptimizeResponse {

    success: boolean;

    optimized_filename: string;

    blocks: any[];

    layout: any;

}

export const optimizeResume = async (

    resumeId: string,

    jobDescription: string,

    selectedSkills: string[]

): Promise<OptimizeResponse> => {

    const response = await api.post(

        "/optimization/optimize",

        {

            resume_id: resumeId,

            job_description: jobDescription,

            selected_skills: selectedSkills

        }

    );

    return response.data;

};