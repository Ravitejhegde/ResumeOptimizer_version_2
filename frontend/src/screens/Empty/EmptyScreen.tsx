import { useState } from "react";

import UploadCard from "../../features/upload/UploadCard";
import JobDescriptionCard from "../../features/job-description/JobDescriptionCard";

import PrimaryButton from "../../shared/ui/Button/PrimaryButton";

import styles from "./EmptyScreen.module.css";

export default function EmptyScreen() {

    const [file, setFile] =
        useState<File | null>(null);

    const [
        jobDescription,
        setJobDescription,
    ] = useState("");

    const canContinue =
        file &&
        jobDescription.trim().length > 20;

    function handleContinue() {

        console.log(file);

        console.log(jobDescription);

    }

    return (

        <div className={styles.page}>

            <div className={styles.container}>

                <div className={styles.header}>

                    <h1 className={styles.title}>

                        ResumeOptimizer

                    </h1>

                    <p className={styles.subtitle}>

                        Upload your resume and paste the job description.

                    </p>

                </div>

                <UploadCard

                    file={file}

                    onFileSelect={setFile}

                />

                <JobDescriptionCard

                    value={jobDescription}

                    onChange={setJobDescription}

                />

                <div
                    className={styles.buttonContainer}
                >

                    <PrimaryButton

                        title="Continue"

                        disabled={!canContinue}

                        onClick={handleContinue}

                    />

                </div>

            </div>

        </div>

    );

}