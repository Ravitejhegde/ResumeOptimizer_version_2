import api from "../api/client";

export const downloadResume = async (
    filename: string
): Promise<void> => {

    const response = await api.get(

        `/download/${filename}`,

        {

            responseType: "blob",

        }

    );

    const blob = new Blob([response.data]);

    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;

    link.download = filename;

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    window.URL.revokeObjectURL(url);

};