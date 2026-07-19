import api from "./api";

export async function optimizeResume(

    resume_filename: string,

    job_description: string,

    selected_skills: string[],

) {

    const response = await api.post(

        "/optimization/optimize",

        {

            resume_filename,

            job_description,

            selected_skills,

        },

    );

    return response.data;

}