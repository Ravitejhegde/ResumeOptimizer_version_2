import api from "../api/client";

export interface UploadResponse {
  resume_id: string;
  filename: string;
  stored_filename: string;
  status: string;
}

export const uploadResume = async (
  file: File,
): Promise<UploadResponse> => {
  const form = new FormData();

  form.append("file", file);

  const response = await api.post<UploadResponse>(
    "/resume/upload",
    form,
  );

  return response.data;
};