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


    // =========================================================
    // ANALYZE RESUME
    // =========================================================

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


            setState(previous => ({
                ...previous,

                atsScore: result.score,

                // IMPORTANT:
                // Save the backend-detected canonical role ID.
                roleId: result.role_id,

                matchedSkills:
                    result.matched_skills,

                missingSkills:
                    result.missing_skills,

                matchedTechnologies:
                    result.matched_technologies,

                missingTechnologies:
                    result.missing_technologies,

                selectedSkills: []
            }));

        } catch (error) {

            console.error(
                "Resume analysis failed:",
                error
            );

            alert(
                "We couldn't analyze your resume. Please try again."
            );

        } finally {

            setLoading(false);

        }
    };


    // =========================================================
    // OPTIMIZE RESUME
    // =========================================================

    const handleOptimize = async () => {

        if (!state.resume) {
            alert("Please upload your resume first.");
            return;
        }

        if (!state.jobDescription.trim()) {
            alert("Please paste the Job Description.");
            return;
        }

        if (!state.roleId) {
            alert(
                "Resume role could not be determined. Please analyze the resume again."
            );
            return;
        }

        if (state.selectedSkills.length === 0) {
            alert(
                "Select at least one missing technology to optimize."
            );
            return;
        }


        try {

            setLoading(true);


            const result = await optimizeResume(
                state.resume.id,
                state.jobDescription,
                state.roleId,
                state.selectedSkills
            );


            setState(previous => ({
                ...previous,

                optimizedFilename:
                    result.optimized_filename,

                previewBlocks:
                    result.blocks,

                previewLayout:
                    result.layout,

                step: "optimization"
            }));


        } catch (error) {

            console.error(
                "Resume optimization failed:",
                error
            );

            alert(
                "We couldn't optimize your resume. Please try again."
            );

        } finally {

            setLoading(false);

        }
    };


    // =========================================================
    // UI
    // =========================================================

    return (
        <div className={styles.workspace}>

            {/* =================================================
                LEFT SIDE
            ================================================= */}

            <section className={styles.left}>

                <UploadDropzone
                    onBrowse={() => {}}
                    onDrop={() => {}}
                />


                {state.resume && (

                    <UploadedResumeCard

                        filename={
                            state.resume.filename
                        }

                        fileSize="Ready for analysis"

                        uploaded

                        onReplace={() => {}}

                        onRemove={() => {

                            setState(previous => ({
                                ...previous,

                                resume: null,

                                atsScore: 0,

                                role: "",

                                roleId: "",

                                experience: 0,

                                matchedSkills: [],

                                missingSkills: [],

                                matchedTechnologies: [],

                                missingTechnologies: [],

                                selectedSkills: []
                            }));

                        }}

                    />

                )}


                <UploadFooter />


                <JobDescriptionEditor

                    value={
                        state.jobDescription
                    }

                    analyzed={
                        state.atsScore > 0
                    }

                    onChange={(value) => {

                        setState(previous => ({
                            ...previous,

                            jobDescription: value,

                            atsScore: 0,

                            role: "",

                            roleId: "",

                            experience: 0,

                            matchedSkills: [],

                            missingSkills: [],

                            matchedTechnologies: [],

                            missingTechnologies: [],

                            selectedSkills: []
                        }));

                    }}


                    onClear={() => {

                        setState(previous => ({
                            ...previous,

                            jobDescription: "",

                            atsScore: 0,

                            role: "",

                            roleId: "",

                            experience: 0,

                            matchedSkills: [],

                            missingSkills: [],

                            matchedTechnologies: [],

                            missingTechnologies: [],

                            selectedSkills: []
                        }));

                    }}

                />


                <JobDescriptionActions

                    loading={loading}

                    onContinue={
                        handleContinueAnalysis
                    }

                />

            </section>


            {/* =================================================
                RIGHT SIDE
            ================================================= */}

            <aside className={styles.right}>

                <ResumeAnalysisCard

                    score={
                        state.atsScore
                    }

                    role={
                        state.roleId
                    }

                    experience={
                        state.experience
                    }

                    matchedTechnologies={
                        state.matchedTechnologies
                    }

                    missingTechnologies={
                        state.missingTechnologies
                    }

                    selectedSkills={
                        state.selectedSkills
                    }


                    // -----------------------------------------
                    // Toggle individual missing technology
                    // -----------------------------------------

                    onSkillToggle={(technology) => {

                        setState(previous => {

                            const exists =
                                previous.selectedSkills.includes(
                                    technology
                                );


                            return {
                                ...previous,

                                selectedSkills: exists

                                    ? previous.selectedSkills.filter(
                                        item =>
                                            item !== technology
                                    )

                                    : [
                                        ...previous.selectedSkills,
                                        technology
                                    ]
                            };

                        });

                    }}


                    // -----------------------------------------
                    // Select all missing technologies
                    // -----------------------------------------

                    onSelectAll={() => {

                        setState(previous => ({
                            ...previous,

                            selectedSkills: [
                                ...previous.missingTechnologies
                            ]
                        }));

                    }}


                    // -----------------------------------------
                    // Clear selected technologies
                    // -----------------------------------------

                    onClearSelection={() => {

                        setState(previous => ({
                            ...previous,

                            selectedSkills: []
                        }));

                    }}


                    // -----------------------------------------
                    // Optimize
                    // -----------------------------------------

                    onOptimize={
                        handleOptimize
                    }


                    optimizing={
                        loading
                    }

                />

            </aside>

        </div>
    );
};


export default AnalysisWorkspace;