import api from "./api";

export async function analyzeResume(

    resume_id: string,

    job_description: string,

) {

    const response = await api.post(

        "/analysis/match",

        {

            resume_id,

            job_description,

        },

    );

    return response.data;

}