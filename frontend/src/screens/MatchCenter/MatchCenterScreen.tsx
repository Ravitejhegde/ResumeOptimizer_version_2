import { useState } from "react";

import UploadSection from "./UploadSection";
import JobDescriptionSection from "./JobDescriptionSection";
import SkillSection from "./SkillSection";
import PreviewSection from "./PreviewSection";

import styles from "./MatchCenterScreen.module.css";

import type { ResumeBlock } from "../../features/resume-editor/types";

export default function MatchCenterScreen() {

    const [resumeFile, setResumeFile] =
        useState<File | null>(null);

    const [resumeId, setResumeId] =
        useState("");

    const [storedFilename, setStoredFilename] =
        useState("");

    const [optimizedFilename, setOptimizedFilename] =
        useState("");

    const [jobDescription, setJobDescription] =
        useState("");

    const [matchedSkills, setMatchedSkills] =
        useState<string[]>([]);

    const [missingSkills, setMissingSkills] =
        useState<string[]>([]);

    const [selectedSkills, setSelectedSkills] =
        useState<string[]>([]);

    const [score, setScore] =
        useState<number | null>(null);

    const [previewBlocks, setPreviewBlocks] =
        useState<ResumeBlock[]>([]);

    return (

        <div className={styles.page}>

            <div className={styles.container}>

                <div className={styles.left}>

                    <UploadSection

                        resumeFile={resumeFile}

                        setResumeFile={setResumeFile}

                        setResumeId={setResumeId}

                        setStoredFilename={setStoredFilename}

                    />

                    <div className={styles.space} />

                    <JobDescriptionSection

                        resumeId={resumeId}

                        jobDescription={jobDescription}

                        setJobDescription={setJobDescription}

                        setScore={setScore}

                        setMatchedSkills={setMatchedSkills}

                        setMissingSkills={setMissingSkills}

                        setSelectedSkills={setSelectedSkills}

                    />

                </div>

                <div className={styles.right}>

                    <SkillSection

                        score={score}

                        storedFilename={storedFilename}

                        jobDescription={jobDescription}

                        matchedSkills={matchedSkills}

                        missingSkills={missingSkills}

                        selectedSkills={selectedSkills}

                        setSelectedSkills={setSelectedSkills}

                        setOptimizedFilename={setOptimizedFilename}

                        setPreviewBlocks={setPreviewBlocks}

                    />

                    <div className={styles.space} />

                    <PreviewSection

                        optimizedFilename={optimizedFilename}

                        previewBlocks={previewBlocks}

                        setPreviewBlocks={setPreviewBlocks}

                    />

                </div>

            </div>

        </div>

    );

}