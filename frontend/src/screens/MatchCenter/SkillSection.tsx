import SkillApprovalCard from "../../features/review-skills/SkillApprovalCard";

import PrimaryButton from "../../shared/ui/Button/PrimaryButton";

import {
    optimizeResume as optimizeResumeApi,
} from "../../services/optimizationApi";

import type { ResumeBlock } from "../../features/resume-editor/types";

type Props = {

    score: number | null;

    storedFilename: string;

    jobDescription: string;

    matchedSkills: string[];

    missingSkills: string[];

    selectedSkills: string[];

    setSelectedSkills: React.Dispatch<
        React.SetStateAction<string[]>
    >;

    setOptimizedFilename: React.Dispatch<
        React.SetStateAction<string>
    >;

    setPreviewBlocks: React.Dispatch<
        React.SetStateAction<ResumeBlock[]>
    >;

};

export default function SkillSection({

    score,

    storedFilename,

    jobDescription,

    matchedSkills,

    missingSkills,

    selectedSkills,

    setSelectedSkills,

    setOptimizedFilename,

    setPreviewBlocks,

}: Props) {

    const suggestedSkills = [

        ...matchedSkills,

        ...missingSkills.filter(

            skill => !matchedSkills.includes(skill)

        ),

    ];

    function toggleSkill(
        skill: string,
    ) {

        setSelectedSkills(previous =>

            previous.includes(skill)

                ? previous.filter(

                      item => item !== skill

                  )

                : [

                      ...previous,

                      skill,

                  ]

        );

    }

    async function optimizeResume() {

        if (!storedFilename) {

            alert(
                "Please upload your resume first."
            );

            return;

        }

        if (!jobDescription.trim()) {

            alert(
                "Please paste the Job Description."
            );

            return;

        }

        try {

            const response =
                await optimizeResumeApi(

                    storedFilename,

                    jobDescription,

                    selectedSkills,

                );

            console.log("API Response:", response);

            if (response.success) {

                const result = response.data;

                console.log("Optimization Result:", result);

                setOptimizedFilename(
                    result.optimized_filename
                );

                setPreviewBlocks(
                    result.blocks ?? 
                    result.preview_blocks ?? 
                    []
                );

                alert(
                    "Resume optimized successfully."
                );

            }

        }

        catch (error: any) {

            console.error(error);

            alert(

                error.response?.data?.detail ??

                error.message ??

                "Optimization failed."

            );

        }

    }

    return (

        <>

            {score !== null && (

                <div

                    style={{

                        marginBottom: 20,

                        fontWeight: 700,

                        fontSize: 22,

                    }}

                >

                    Match Score : {score}%

                </div>

            )}

            <SkillApprovalCard

                skills={suggestedSkills}

                selected={selectedSkills}

                onToggle={toggleSkill}

            />

            <div style={{ height: 24 }} />

            <PrimaryButton

                title="Optimize Resume"

                onClick={optimizeResume}

            />

        </>

    );

}