import { useState } from "react";

import styles from "./AnalysisWorkspace.module.css";

import UploadDropzone from "../../features/upload/components/UploadDropzone/UploadDropzone";
import UploadedResumeCard from "../../features/upload/components/UploadedResumeCard/UploadedResumeCard";
import UploadFooter from "../../features/upload/components/UploadFooter/UploadFooter";

import JobDescriptionEditor from "../../features/job-description/components/JobDescriptionEditor/JobDescriptionEditor";
import JobDescriptionActions from "../../features/job-description/components/JobDescriptionActions/JobDescriptionActions";

import ResumeAnalysisCard from "../../features/analysis/components/ResumeAnalysisCard/ResumeAnalysisCard";

import { analyzeResume } from "../../services/analysis/analysis.service";
import { optimizeResume } from "../../services/optimization/optimization.service";

import { useWorkspace } from "../../store/useWorkspace";

const AnalysisWorkspace = () => {

    const {
        state,
        setState
    } = useWorkspace();

    const [loading, setLoading] = useState(false);

    const handleContinueAnalysis = async () => {

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

            const result = await analyzeResume({

                resume_id: state.resume.id,

                job_description: state.jobDescription

            });

            console.log("Analysis Response:", result);

            setState(previous => ({

                ...previous,

                atsScore: result.score,

                matchedSkills: result.matched_skills,

                missingSkills: result.missing_skills

            }));

        }

        catch (error) {

            console.error(error);

            alert("Analysis failed.");

        }

        finally {

            setLoading(false);

        }

    };

    const handleOptimize = async () => {

        if (!state.resume) {

            alert("Upload resume first.");

            return;

        }

        if (!state.jobDescription.trim()) {

            alert("Please paste Job Description.");

            return;

        }

        if (state.selectedSkills.length === 0) {

            alert("Please select at least one skill.");

            return;

        }

        try {

            setLoading(true);

            const result = await optimizeResume(

                state.resume.id,

                state.jobDescription,

                state.selectedSkills

            );

            console.log("Optimization Response:", result);

            setState(previous => ({

                ...previous,

                optimizedFilename: result.optimized_filename,

                previewBlocks: result.blocks,

                previewLayout: result.layout,

                step: "optimization"

            }));

        }

        catch (error) {

            console.error(error);

            alert("Optimization failed.");

        }

        finally {

            setLoading(false);

        }

    };

    return (

        <div className={styles.workspace}>

            <section className={styles.left}>

                <UploadDropzone
                    onBrowse={() => {}}
                    onDrop={() => {}}
                />

                {state.resume && (

                    <UploadedResumeCard
                        filename={state.resume.filename}
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

                <UploadFooter />

                <JobDescriptionEditor

                    value={state.jobDescription}

                    analyzed={state.atsScore > 0}

                    onChange={(value) =>

                        setState(previous => ({

                            ...previous,

                            jobDescription: value

                        }))

                    }

                    onClear={() =>

                        setState(previous => ({

                            ...previous,

                            jobDescription: ""

                        }))

                    }

                />

                <JobDescriptionActions

                    loading={loading}

                    onContinue={handleContinueAnalysis}

                />

            </section>

            <aside className={styles.right}>

                <ResumeAnalysisCard

                    score={state.atsScore}

                    role={state.role}

                    experience={state.experience}

                    matchedSkills={state.matchedSkills}

                    missingSkills={state.missingSkills}

                    selectedSkills={state.selectedSkills}

                    onSkillToggle={(skill) => {

                        setState(previous => {

                            const exists = previous.selectedSkills.includes(skill);

                            return {

                                ...previous,

                                selectedSkills: exists
                                    ? previous.selectedSkills.filter(item => item !== skill)
                                    : [...previous.selectedSkills, skill]

                            };

                        });

                    }}

                    onSelectAll={() => {

                        setState(previous => ({

                            ...previous,

                            selectedSkills: [...previous.missingSkills]

                        }));

                    }}

                    onClearSelection={() => {

                        setState(previous => ({

                            ...previous,

                            selectedSkills: []

                        }));

                    }}

                    onOptimize={handleOptimize}

                    optimizing={loading}

                />

            </aside>

        </div>

    );

};

export default AnalysisWorkspace;