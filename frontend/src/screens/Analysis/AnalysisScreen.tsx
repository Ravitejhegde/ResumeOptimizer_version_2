import styles from "./AnalysisScreen.module.css";

export default function AnalysisScreen() {
    return (
        <main className={styles.page}>
            <div className={styles.card}>

                <div className={styles.spinner}></div>

                <h1>Analyzing Your Resume</h1>

                <p>
                    Please wait while ResumeOptimizer analyzes
                    your resume and compares it with the job
                    description.
                </p>

                <div className={styles.steps}>

                    <div className={styles.step}>
                        ✓ Reading Resume
                    </div>

                    <div className={styles.step}>
                        ✓ Extracting Resume Skills
                    </div>

                    <div className={styles.step}>
                        ✓ Reading Job Description
                    </div>

                    <div className={styles.step}>
                        ✓ Detecting Required Skills
                    </div>

                    <div className={styles.step}>
                        ✓ Calculating ATS Match Score
                    </div>

                    <div className={styles.step}>
                        ✓ Preparing Optimization Suggestions
                    </div>

                </div>

            </div>
        </main>
    );
}