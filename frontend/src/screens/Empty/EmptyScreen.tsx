import styles from "../../app/App.module.css";

import Container from "../../shared/ui/Container/Container";
import Card from "../../shared/ui/Card/Card";
import UploadArea from "../../shared/ui/UploadArea/UploadArea";
import Button from "../../shared/ui/Button/Button";
import JobDescriptionAnalyzer from "../../features/job-description/JobDescriptionAnalyzer";

import { useApp } from "../../context/AppContext";
import { matchResume } from "../../services/analysisService";

export default function EmptyScreen() {

    const {

        resume,

        jobDescription,

        setMatchResult,

        setLoading,

        setError,

        loading,

        setState,

    } = useApp();

    async function handleAnalyze() {

        if (!resume) {

            alert("Please upload a resume.");

            return;

        }

        if (!jobDescription.trim()) {

            alert("Please paste a Job Description.");

            return;

        }

        try {

            setLoading(true);

            setError("");

            const result = await matchResume(

                resume.resume_id,

                jobDescription

            );

            setMatchResult(result);

            setState("MATCH");

        }

        catch (error) {

            console.error(error);

            alert("Unable to analyze resume.");

        }

        finally {

            setLoading(false);

        }

    }

    return (

        <main className={styles.page}>

            <Container>

                <Card>

                    <div className={styles.hero}>

                        <h1 className={styles.title}>

                            ResumeOptimizer

                        </h1>

                        <p className={styles.subtitle}>

                            Optimize your resume for ATS and AI-powered hiring systems.

                        </p>

                    </div>

                    <section className={styles.section}>

                        <label className={styles.label}>

                            📄 Step 1 · Upload Resume

                        </label>

                        <UploadArea />

                    </section>

                    <section className={styles.section}>

                        <label className={styles.label}>

                            📝 Step 2 · Job Description

                        </label>

                        <JobDescriptionAnalyzer />

                    </section>

                    <section className={styles.section}>

                        <Button
                            onClick={handleAnalyze}
                        >

                            {

                                loading

                                    ? "Analyzing..."

                                    : "Analyze Resume"

                            }

                        </Button>

                    </section>

                    <div className={styles.footer}>

                        <span>

                            {

                                resume

                                    ? `✅ ${resume.original_filename}`

                                    : "📄 Resume Not Uploaded"

                            }

                        </span>

                        <span>

                            {

                                jobDescription.trim()

                                    ? "✅ Job Description Ready"

                                    : "📝 Waiting for Job Description"

                            }

                        </span>

                    </div>

                </Card>

            </Container>

        </main>

    );

}