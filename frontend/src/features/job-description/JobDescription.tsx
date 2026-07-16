import { useState } from "react";

import { analyzeJobDescription } from "../../services/analysisService";
import { useApp } from "../../context/AppContext";

import "./JobDescription.css";

export default function JobDescription() {

    const {

        jobDescription,
        setJobDescription,

        setJdAnalysis,

        loading,
        setLoading,

        error,
        setError,

        setState,

    } = useApp();

    const [success, setSuccess] =
        useState(false);

    async function handleAnalyze() {

        if (!jobDescription.trim()) {

            setError(
                "Please paste the Job Description."
            );

            return;

        }

        try {

            setLoading(true);
            setError("");
            setSuccess(false);

            const result =
                await analyzeJobDescription(
                    jobDescription
                );

            setJdAnalysis(result);

            setSuccess(true);

            setState("JD_READY");

        } catch {

            setError(
                "Unable to analyze Job Description."
            );

        } finally {

            setLoading(false);

        }

    }

    return (

        <div className="jd-container">

            <h2>

                Job Description

            </h2>

            <p>

                Paste the complete job description below.

            </p>

            <textarea

                className="jd-textarea"

                value={jobDescription}

                onChange={(e) => {

                    setJobDescription(
                        e.target.value
                    );

                    setSuccess(false);

                }}

                placeholder="Paste Job Description..."

            />

            {

                error &&

                <div className="jd-error">

                    {error}

                </div>

            }

            {

                success &&

                <div className="jd-success">

                    Job Description analyzed successfully.

                </div>

            }

            <button

                className="jd-button"

                disabled={loading}

                onClick={handleAnalyze}

            >

                {

                    loading

                        ? "Analyzing..."

                        : "Analyze Job Description"

                }

            </button>

        </div>

    );

}