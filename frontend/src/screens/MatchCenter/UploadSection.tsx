import UploadCard from "../../features/upload/UploadCard";

import { uploadResume } from "../../services/resumeApi";

type Props = {

    resumeFile: File | null;

    setResumeFile: React.Dispatch<
        React.SetStateAction<File | null>
    >;

    setResumeId: React.Dispatch<
        React.SetStateAction<string>
    >;

    setStoredFilename: React.Dispatch<
        React.SetStateAction<string>
    >;

};

export default function UploadSection({

    resumeFile,

    setResumeFile,

    setResumeId,

    setStoredFilename,

}: Props) {

    async function handleFileSelect(file: File) {

        setResumeFile(file);

        try {

            const response = await uploadResume(file);

            console.log("Upload Response:", response);

            if (!response.success) {

                throw new Error("Upload failed.");

            }

            setResumeId(
                response.data.resume_id
            );

            setStoredFilename(
                response.data.stored_filename
            );

            console.log(
                "Resume ID:",
                response.data.resume_id
            );

            console.log(
                "Stored Filename:",
                response.data.stored_filename
            );

            alert("Resume uploaded successfully.");

        }

        catch (error: any) {

            console.error(error);

            alert(

                error.response?.data?.detail ??

                error.message ??

                "Resume upload failed."

            );

        }

    }

    return (

        <UploadCard

            file={resumeFile}

            onFileSelect={
                handleFileSelect
            }

        />

    );

}