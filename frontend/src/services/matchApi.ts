import api from "./api";

export async function analyzeResume(
    resumeId: string,
    jobDescription: string,
) {

    const response = await api.post(
        "/analysis/match",
        {

            resume_id: resumeId,

            job_description: jobDescription,

        }
    );

    return response.data;

}