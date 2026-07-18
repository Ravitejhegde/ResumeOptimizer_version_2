import JobDescriptionCard from "../../features/job-description/JobDescriptionCard";

import PrimaryButton from "../../shared/ui/Button/PrimaryButton";

import { analyzeResume } from "../../services/analysisApi";

type Props = {

    resumeId: string;

    jobDescription: string;

    setJobDescription: React.Dispatch<
        React.SetStateAction<string>
    >;

    setScore: React.Dispatch<
        React.SetStateAction<number | null>
    >;

    setMatchedSkills: React.Dispatch<
        React.SetStateAction<string[]>
    >;

    setMissingSkills: React.Dispatch<
        React.SetStateAction<string[]>
    >;

    setSelectedSkills: React.Dispatch<
        React.SetStateAction<string[]>
    >;

};

export default function JobDescriptionSection({

    resumeId,

    jobDescription,

    setJobDescription,

    setScore,

    setMatchedSkills,

    setMissingSkills,

    setSelectedSkills,

}: Props) {

    async function continueToOptimization() {

        if (!resumeId) {

            alert("Please upload your resume.");

            return;

        }

        if (!jobDescription.trim()) {

            alert("Please paste the Job Description.");

            return;

        }

        try {

            const response =
                await analyzeResume(
                    resumeId,
                    jobDescription,
                );

            setScore(
                response.score
            );

            setMatchedSkills(
                response.matched_skills
            );

            setMissingSkills(
                response.missing_skills
            );

            setSelectedSkills(
                response.matched_skills
            );

        }

        catch (error) {

            console.error(error);

            alert(
                "Analysis failed."
            );

        }

    }

    return (

        <>

            <JobDescriptionCard

                value={jobDescription}

                onChange={
                    setJobDescription
                }

            />

            <div style={{ height: 24 }} />

            <PrimaryButton

                title="Continue to Optimization"

                onClick={
                    continueToOptimization
                }

            />

        </>

    );

}