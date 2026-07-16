import { analyzeJobDescription } from "../../services/analysisService";

import { useApp } from "../../context/AppContext";

import TextArea from "../../shared/ui/TextArea/TextArea";
import Button from "../../shared/ui/Button/Button";

import styles from "./JobDescriptionAnalyzer.module.css";

export default function JobDescriptionAnalyzer() {

    const {

        jobDescription,
        setJobDescription,

        jdAnalysis,
        setJdAnalysis,

        loading,
        setLoading,

        setError,

        setState,

    } = useApp();

    async function analyze() {

        if (!jobDescription.trim()) {

            alert("Please paste a Job Description.");

            return;

        }

        try {

            setLoading(true);

            setError("");

            const result =
                await analyzeJobDescription(
                    jobDescription
                );

            setJdAnalysis(result);

            setState("JD_READY");

        }

        catch (error) {

            console.error(error);

            setError(
                "Failed to analyze Job Description."
            );

        }

        finally {

            setLoading(false);

        }

    }

    if (jdAnalysis) {

        return (

            <div className={styles.summaryCard}>

                <h2>

                    Job Description Analysis

                </h2>

                <p>

                    <strong>Job Title:</strong>{" "}

                    {jdAnalysis.title}

                </p>

                <p>

                    <strong>Experience:</strong>{" "}

                    {jdAnalysis.experience}

                </p>

                <h3>

                    Required Skills

                </h3>

                <div className={styles.skills}>

                    {

                        jdAnalysis.skills.map(

                            (skill) => (

                                <span

                                    key={skill}

                                    className={styles.skill}

                                >

                                    {skill}

                                </span>

                            )

                        )

                    }

                </div>

                <Button

                    onClick={() => {

                        setJdAnalysis(null);

                        setState("RESUME_UPLOADED");

                    }}

                >

                    Edit Job Description

                </Button>

            </div>

        );

    }

    return (

        <>

            <TextArea

                value={jobDescription}

                onChange={(e) =>

                    setJobDescription(

                        e.target.value

                    )

                }

                placeholder="Paste Job Description..."

                rows={12}

            />

            <Button

                onClick={analyze}

            >

                {

                    loading

                        ? "Analyzing..."

                        : "Analyze Job Description"

                }

            </Button>

        </>

    );

}