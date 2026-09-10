import { useState } from "react";

import UploadDropzone from "../../features/upload/components/UploadDropzone/UploadDropzone";
import UploadedResumeCard from "../../features/upload/components/UploadedResumeCard/UploadedResumeCard";

import JobDescriptionEditor from "../../features/job-description/components/JobDescriptionEditor/JobDescriptionEditor";

import { analyzeResume } from "../../services/analysis/analysis.service";
import { optimizeResume } from "../../services/optimization/optimization.service";

import { useWorkspace } from "../../store/useWorkspace";

import styles from "./FreeOptimization.module.css";


const FreeOptimization = () => {

    const {
        state,
        setState
    } = useWorkspace();

    const [loading, setLoading] = useState(false);

    const handleOptimize = async () => {

        if (!state.resume) {

            alert("Please upload your resume.");

            return;

        }

        if (!state.jobDescription.trim()) {

            alert("Please paste the Job Description.");

            return;

        }

        try {

            setLoading(true);

            /*
             * First run the existing analysis API.
             *
             * We keep this internally because the backend
             * optimization contract currently accepts
             * selected_skills.
             *
             * The user does NOT need to interact with
             * the skill-selection UI.
             */

            const analysis = await analyzeResume({

                resume_id: state.resume.id,

                job_description:
                    state.jobDescription

            });

            /*
             * For the free flow, use the backend's
             * detected missing skills as optimization
             * targets automatically.
             */

            const selectedSkills =
                analysis.missing_skills ?? [];

            const optimization =
    await optimizeResume(

        state.resume.id,

        state.jobDescription,

        analysis.role_id,

        selectedSkills

    );

            setState(previous => ({

                ...previous,

                atsScore:
                    analysis.score ?? 0,

                matchedSkills:
                    analysis.matched_skills ?? [],

                missingSkills:
                    analysis.missing_skills ?? [],

                selectedSkills,

                optimizedFilename:
    optimization.output_path,

optimizedResumeId:
    optimization.generated_resume_id,

previewBlocks:
    [],

previewLayout:
    null,

                step: "optimization"

            }));

        }

        catch (error) {

            console.error(
                "Free optimization failed:",
                error
            );

            alert(
                "We couldn't optimize your resume. Please try again."
            );

        }

        finally {

            setLoading(false);

        }

    };


    return (

        <main className={styles.page}>

            <section className={styles.hero}>

                <span className={styles.eyebrow}>
                    FREE SAMPLE OPTIMIZATION
                </span>

                <h1>
                    Same Resume.
                    <br />
                    Smarter Words.
                </h1>

                <p>
                    Upload your existing DOCX resume,
                    paste a Job Description, and see
                    how ResumeOptimizer improves the
                    wording for that specific role.
                </p>

            </section>


            <section className={styles.workspace}>

                <div className={styles.inputCard}>

                    <div className={styles.sectionHeader}>

                        <span className={styles.step}>
                            01
                        </span>

                        <div>

                            <h2>
                                Upload your resume
                            </h2>

                            <p>
                                We preserve your original
                                document structure.
                            </p>

                        </div>

                    </div>


                    {!state.resume ? (

                        <UploadDropzone

                            onBrowse={() => {}}

                            onDrop={() => {}}

                        />

                    ) : (

                        <UploadedResumeCard

                            filename={
                                state.resume.filename
                            }

                            fileSize="Uploaded"

                            uploaded

                            onReplace={() => {}}

                            onRemove={() => {

                                setState(previous => ({

                                    ...previous,

                                    resume: null

                                }));

                            }}

                        />

                    )}

                </div>


                <div className={styles.inputCard}>

                    <div className={styles.sectionHeader}>

                        <span className={styles.step}>
                            02
                        </span>

                        <div>

                            <h2>
                                Add the Job Description
                            </h2>

                            <p>
                                Tell us which role you're
                                applying for.
                            </p>

                        </div>

                    </div>


                    <JobDescriptionEditor

                        value={
                            state.jobDescription
                        }

                        analyzed={false}

                        onChange={(value) => {

                            setState(previous => ({

                                ...previous,

                                jobDescription: value

                            }));

                        }}

                        onClear={() => {

                            setState(previous => ({

                                ...previous,

                                jobDescription: ""

                            }));

                        }}

                    />

                </div>


                <div className={styles.actionArea}>

                    <button

                        type="button"

                        className={styles.optimizeButton}

                        disabled={loading}

                        onClick={handleOptimize}

                    >

                        {loading
                            ? "Optimizing..."
                            : "Optimize My Resume"
                        }

                    </button>

                    <p className={styles.disclaimer}>
                        Free sample · No credit card required
                    </p>

                </div>

            </section>

        </main>

    );

};


export default FreeOptimization;