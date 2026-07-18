import { useState } from "react";

import { uploadResume } from "../../services/resumeApi";

import UploadCard from "../../features/upload/UploadCard";
import JobDescriptionCard from "../../features/job-description/JobDescriptionCard";
import PrimaryButton from "../../shared/ui/Button/PrimaryButton";

import styles from "./EmptyScreen.module.css";

export default function EmptyScreen() {

    const [file, setFile] =
        useState<File | null>(null);

    const [jobDescription, setJobDescription] =
        useState("");

    const [uploading, setUploading] =
        useState(false);

    const [resumeFilename, setResumeFilename] =
        useState("");

    async function handleFileSelected(
        selected: File,
    ) {

        setFile(selected);

        setUploading(true);

        try {

            const response =
                await uploadResume(selected);

            setResumeFilename(
                response.data.stored_filename
            );

        }

        catch (error) {

            console.error(error);

            alert("Upload failed.");

        }

        finally {

            setUploading(false);

        }

    }

    const canContinue =

        resumeFilename.length > 0 &&

        jobDescription.trim().length > 20;

    function handleContinue() {

        console.log({

            stored_filename:
                resumeFilename,

            job_description:
                jobDescription,

        });

    }

    return (

        <div className={styles.page}>

            <div className={styles.container}>

                <div className={styles.header}>

                    <h1 className={styles.title}>

                        Resume Optimizer

                    </h1>

                    <p className={styles.subtitle}>

                        Optimize your resume for any job description while preserving formatting.

                    </p>

                </div>

                <UploadCard

                    file={file}

                    onFileSelect={
                        handleFileSelected
                    }

                />

                <JobDescriptionCard

                    value={jobDescription}

                    onChange={
                        setJobDescription
                    }

                />

                <div
                    className={
                        styles.buttonContainer
                    }
                >

                    <PrimaryButton

                        title={
                            uploading
                                ? "Uploading..."
                                : "Continue →"
                        }

                        disabled={
                            uploading ||
                            !canContinue
                        }

                        onClick={
                            handleContinue
                        }

                    />

                </div>

            </div>

        </div>

    );

}