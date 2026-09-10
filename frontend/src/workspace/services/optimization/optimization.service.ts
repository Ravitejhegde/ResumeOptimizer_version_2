import api from "../api/client";

export interface OptimizeResponse {
    success: boolean;
    message: string;
    output_path: string;
    generated_resume_id: string;
}


export const optimizeResume = async (

    resumeId: string,

    jobDescription: string,

    roleId: string,

    selectedSkills: string[]

): Promise<OptimizeResponse> => {

    const response = await api.post(

        "/optimization/optimize",

        {

            resume_id: resumeId,

            job_description: jobDescription,

            role_id: roleId,

            selected_skills: selectedSkills

        }

    );

    return response.data;

};