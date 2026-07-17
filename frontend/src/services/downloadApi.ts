import api from "./api";

export async function downloadResume(
    filename: string
) {
    const response = await api.get(
        `/resume/download/${filename}`,
        {
            responseType: "blob",
        }
    );

    return response.data;
}