import { useState } from "react";

import { useWorkspace } from "../../store/useWorkspace";

import DocumentViewer from "../../features/preview/components/DocumentViewer/DocumentViewer";
import styles from "./OptimizationWorkspace.module.css";

const OptimizationWorkspace = () => {
    const { state } = useWorkspace();

    const [showDetails, setShowDetails] = useState(false);

    const selectedCount = state.selectedSkills.length;

    return (
        <div className={styles.workspace}>

            {/* =================================================
               Header
            ================================================= */}

            <header className={styles.header}>

                <div>
                    <div className={styles.eyebrow}>
                        RESUME OPTIMIZATION
                    </div>

                    <h1>
                        Your optimized resume is ready
                    </h1>

                    <p>
                        We strengthened your resume for the
                        target job while preserving its structure.
                    </p>
                </div>

                <div className={styles.status}>
                    <span className={styles.statusDot} />
                    Optimization complete
                </div>

            </header>

            {/* =================================================
               Main Workspace
            ================================================= */}

            <main className={styles.main}>

                {/* ---------------------------------------------
                   Document
                --------------------------------------------- */}

                <section className={styles.documentSection}>

                    <div className={styles.sectionHeader}>

                        <div>
                            <span className={styles.sectionLabel}>
                                PREVIEW
                            </span>

                            <h2>
                                {state.optimizedFilename ||
                                    "Optimized Resume"}
                            </h2>
                        </div>

                        <span className={styles.preserved}>
                            Formatting preserved
                        </span>

                    </div>

                    <DocumentViewer
    blocks={state.previewBlocks}
    filename={state.optimizedFilename}
    resumeOutputId={state.optimizedResumeId}
/>

                </section>

                {/* ---------------------------------------------
                   Summary
                --------------------------------------------- */}

                <aside className={styles.sidebar}>

                    <div className={styles.scoreCard}>

                        <span className={styles.cardLabel}>
                            ATS SCORE
                        </span>

                        <div className={styles.scoreRow}>

                            <strong>
                                {state.atsScore}
                            </strong>

                            <span>
                                / 100
                            </span>

                        </div>

                        <div className={styles.scoreTrack}>

                            <div
                                className={styles.scoreFill}
                                style={{
                                    width: `${Math.min(
                                        state.atsScore,
                                        100
                                    )}%`,
                                }}
                            />

                        </div>

                        <p>
                            Your resume has been aligned with
                            the supplied job description.
                        </p>

                    </div>

                    {/* -----------------------------------------
                       Improvements
                    ----------------------------------------- */}

                    <div className={styles.card}>

                        <div className={styles.cardHeader}>

                            <div>
                                <span className={styles.cardLabel}>
                                    OPTIMIZATION
                                </span>

                                <h3>
                                    What changed
                                </h3>
                            </div>

                            <span className={styles.count}>
                                {selectedCount}
                            </span>

                        </div>

                        <div className={styles.list}>

                            {state.selectedSkills.length > 0 ? (

                                state.selectedSkills.map((skill) => (

                                    <div
                                        className={styles.listItem}
                                        key={skill}
                                    >

                                        <span className={styles.check}>
                                            ✓
                                        </span>

                                        <span>
                                            {skill}
                                        </span>

                                    </div>

                                ))

                            ) : (

                                <div className={styles.empty}>
                                    Resume optimized using the
                                    selected optimization targets.
                                </div>

                            )}

                        </div>

                    </div>

                    {/* -----------------------------------------
                       Original analysis
                    ----------------------------------------- */}

                    <div className={styles.card}>

                        <button
                            className={styles.detailsButton}
                            onClick={() =>
                                setShowDetails(
                                    previous => !previous
                                )
                            }
                        >

                            <span>
                                Analysis details
                            </span>

                            <span>
                                {showDetails ? "−" : "+"}
                            </span>

                        </button>

                        {showDetails && (

                            <div className={styles.details}>

                                <div>
                                    <span>
                                        Matched skills
                                    </span>

                                    <strong>
                                        {state.matchedSkills.length}
                                    </strong>
                                </div>

                                <div>
                                    <span>
                                        Target role
                                    </span>

                                    <strong>
                                        {state.role || "Detected from resume"}
                                    </strong>
                                </div>

                                <div>
                                    <span>
                                        Experience
                                    </span>

                                    <strong>
                                        {state.experience
                                            ? `${state.experience} years`
                                            : "Detected from resume"}
                                    </strong>
                                </div>

                            </div>

                        )}

                    </div>

                    {/* -----------------------------------------
                       Download
                    ----------------------------------------- */}

                    <div className={styles.nextStep}>

                        <h3>
                            Ready to apply?
                        </h3>

                        <p>
                            Download your optimized resume
                            and use it for your application.
                        </p>

                        <button
                            className={styles.downloadButton}
                            onClick={() => {
                                const event =
                                    new CustomEvent(
                                        "resumeoptimizer:download"
                                    );

                                window.dispatchEvent(event);
                            }}
                        >
                            Download optimized DOCX
                        </button>

                        <button
                            className={styles.secondaryButton}
                            onClick={() => {
                                window.scrollTo({
                                    top: 0,
                                    behavior: "smooth",
                                });
                            }}
                        >
                            Review resume
                        </button>

                    </div>

                </aside>

            </main>

        </div>
    );
};

export default OptimizationWorkspace;
