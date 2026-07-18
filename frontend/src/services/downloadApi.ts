import api from "./api";

export function downloadResume(
    filename: string,
) {

    return api.get(
        `/resume/download/${filename}`,
        {
            responseType: "blob",
        },
    );

}