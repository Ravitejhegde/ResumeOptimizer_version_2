import api from "./api";

export interface UploadResponse {

    success: boolean;

    data: {

        resume_id: string;

        stored_filename: string;

    };

}

export async function uploadResume(
    file: File,
): Promise<UploadResponse> {

    const formData = new FormData();

    formData.append(
        "file",
        file,
    );

    const response = await api.post<UploadResponse>(

        "/resume/upload",

        formData,

        {

            headers: {

                "Content-Type":
                    "multipart/form-data",

            },

        },

    );

    console.log(
        "Upload API Response:",
        response.data,
    );

    return response.data;

}