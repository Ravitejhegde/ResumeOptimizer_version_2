import { useState } from "react";

import type { JobAnalysis } from "../../types/jobDescription";

import { analyzeJobDescription } from "../../services/jobDescriptionApi";

import TextArea from "../../shared/ui/TextArea/TextArea";
import Button from "../../shared/ui/Button/Button";

import styles from "./JobDescriptionAnalyzer.module.css";

export default function JobDescriptionAnalyzer() {

    const [text, setText] = useState("");

    const [loading, setLoading] = useState(false);

    const [analysis, setAnalysis] =
        useState<JobAnalysis | null>(null);

    async function analyze() {

    if (!text.trim()) return;

    try {

        setLoading(true);

        const result =
            await analyzeJobDescription(text);

        console.log("API Response:", result);

        setAnalysis(result);

    }

    catch (error: any) {

    console.error(error);

    if (error.response) {

        console.log("Status:", error.response.status);

        console.log("Data:", error.response.data);

    }

    alert("Failed to analyze Job Description.");

}

    finally {

        setLoading(false);

    }

}

    if (analysis) {

        return (

            <div className={styles.summaryCard}>

                <h2>

                    {analysis.title}

                </h2>

                <p>

                    Experience :
                    {" "}
                    {analysis.experience}

                </p>

                <h3>

                    Required Skills

                </h3>

                <div className={styles.skills}>

                    {

                        analysis.skills.map(skill => (

                            <span
                                key={skill}
                                className={styles.skill}
                            >

                                {skill}

                            </span>

                        ))

                    }

                </div>

                <Button

                    onClick={() => setAnalysis(null)}

                >

                    Edit Job Description

                </Button>

            </div>

        );

    }

    return (

        <>

            <TextArea

                value={text}

                onChange={(e) =>
                    setText(e.target.value)
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