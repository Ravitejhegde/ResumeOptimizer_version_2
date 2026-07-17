import api from "./api";

export interface OptimizeRequest {
    stored_filename: string;
    job_description: string;
}

export async function optimizeResume(
    request: OptimizeRequest
) {
    const response = await api.post(
        "/optimization/optimize",
        request
    );

    return response.data;
}