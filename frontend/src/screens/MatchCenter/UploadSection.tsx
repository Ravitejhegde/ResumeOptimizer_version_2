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

    async function handleFileSelect(
        file: File,
    ) {

        setResumeFile(file);

        try {

            const response =
                await uploadResume(file);

            setResumeId(
                response.data.resume_id,
            );

            setStoredFilename(
                response.data.stored_filename,
            );

        }

        catch (error) {

            console.error(error);

            alert(
                "Resume upload failed.",
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