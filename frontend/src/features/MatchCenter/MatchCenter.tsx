import { matchResume } from "../../services/analysisService";
import { useApp } from "../../context/AppContext";

import ScoreCard from "./ScoreCard";
import SkillList from "./SkillList";

import "./MatchCenter.css";

export default function MatchCenter() {

    const {

        resume,
        jobDescription,

        matchResult,
        setMatchResult,

        loading,
        setLoading,

        error,
        setError,

        setState,

    } = useApp();

    async function handleMatch() {

        if (!resume) {

            setError("Please upload a resume.");

            return;

        }

        if (!jobDescription.trim()) {

            setError("Please paste a Job Description.");

            return;

        }

        try {

            setLoading(true);

            setError("");

            setState("ANALYZING");

            const result = await matchResume(

                resume.resume_id,

                jobDescription

            );

            setMatchResult(result);

            setState("MATCH");

        }

        catch (error) {

            console.error(error);

            setError(
                "Unable to generate match report."
            );

        }

        finally {

            setLoading(false);

        }

    }

    return (

        <div className="match-center">

            <h2>

                Resume Match Center

            </h2>

            {

                error && (

                    <div className="match-error">

                        {error}

                    </div>

                )

            }

            <button

                className="match-button"

                disabled={loading}

                onClick={handleMatch}

            >

                {

                    loading

                        ? "Matching..."

                        : "Generate Match Report"

                }

            </button>

            {

                matchResult && (

                    <>

                        <ScoreCard
                            score={matchResult.score}
                        />

                        <SkillList
                            title="Matched Skills"
                            skills={matchResult.matched_skills}
                        />

                        <SkillList
                            title="Missing Skills"
                            skills={matchResult.missing_skills}
                        />

                        <SkillList
                            title="Extra Skills"
                            skills={matchResult.extra_skills}
                        />

                    </>

                )

            }

        </div>

    );

}