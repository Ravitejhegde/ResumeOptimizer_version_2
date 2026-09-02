import styles from "./FreeSample.module.css";

interface FreeSampleProps {
    onStart: () => void;
}

const FreeSample = ({ onStart }: FreeSampleProps) => {
    return (
        <div className={styles.page}>
            <section className={styles.hero}>
                <div className={styles.badge}>
                    FREE RESUME SAMPLE
                </div>

                <h1 className={styles.title}>
                    Make your existing resume
                    <span> smarter for the job.</span>
                </h1>

                <p className={styles.description}>
                    Upload your existing DOCX resume and paste a job
                    description. ResumeOptimizer analyzes the match and
                    shows you where your resume can improve.
                </p>

                <div className={styles.actions}>
                    <button
                        type="button"
                        className={styles.primaryButton}
                        onClick={onStart}
                    >
                        Try Free Sample
                    </button>

                    <span className={styles.note}>
                        No resume builder. No formatting rebuild.
                    </span>
                </div>

                <div className={styles.trust}>
                    <div>
                        <strong>DOCX</strong>
                        <span>Existing resume</span>
                    </div>

                    <div>
                        <strong>60 sec</strong>
                        <span>Simple workflow</span>
                    </div>

                    <div>
                        <strong>ATS</strong>
                        <span>Job matching</span>
                    </div>
                </div>
            </section>

            <section className={styles.preview}>
                <div className={styles.previewHeader}>
                    <span>ResumeOptimizer</span>

                    <span className={styles.previewStatus}>
                        Sample analysis
                    </span>
                </div>

                <div className={styles.previewBody}>
                    <div className={styles.document}>
                        <div className={styles.documentLineLarge} />
                        <div className={styles.documentLine} />
                        <div className={styles.documentLineShort} />

                        <div className={styles.documentSection} />

                        <div className={styles.documentLine} />
                        <div className={styles.documentLine} />
                        <div className={styles.documentLineShort} />

                        <div className={styles.documentSection} />

                        <div className={styles.documentLine} />
                        <div className={styles.documentLineShort} />
                    </div>

                    <div className={styles.scoreCard}>
                        <span>ATS MATCH</span>

                        <strong>82%</strong>

                        <p>
                            See how your resume matches the
                            target job.
                        </p>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default FreeSample;