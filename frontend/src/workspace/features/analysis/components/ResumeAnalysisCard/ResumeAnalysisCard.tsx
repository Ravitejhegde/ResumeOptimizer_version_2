import Card from "../../../../components/ui/Card/Card";
import Button from "../../../../components/ui/Button/Button";

import ATSScoreCard from "../ATSScoreCard/ATSScoreCard";
import RoleCard from "../RoleCard/RoleCard";
import ExperienceCard from "../ExperienceCard/ExperienceCard";
import SkillGroup from "../SkillGroup/SkillGroup";

import styles from "./ResumeAnalysisCard.module.css";

import type { ResumeAnalysisCardProps } from "./ResumeAnalysisCard.types";

const ResumeAnalysisCard = ({
    score,
    role,
    experience,
    matchedTechnologies,
    missingTechnologies,
    selectedSkills,
    onSkillToggle,
    onSelectAll,
    onClearSelection,
    onOptimize,
    optimizing = false
}: ResumeAnalysisCardProps) => {
    return (
        <Card className={styles.container}>

            <h2 className={styles.title}>
                Resume Analysis
            </h2>

            <ATSScoreCard
                score={score}
            />

            <RoleCard
                role={role}
            />

            <ExperienceCard
                years={experience}
            />

            <SkillGroup
                title="Matched Technologies"
                skills={matchedTechnologies}
                variant="success"
            />

            <SkillGroup
                title="Missing Technologies"
                skills={missingTechnologies}
                variant="danger"
                selectable
                selected={selectedSkills}
                onToggle={onSkillToggle}
            />

            <div className={styles.actions}>

                <Button
                    variant="outline"
                    onClick={onSelectAll}
                >
                    Select All
                </Button>

                <Button
                    variant="ghost"
                    onClick={onClearSelection}
                >
                    Clear
                </Button>

            </div>

            <Button
                fullWidth
                size="lg"
                loading={optimizing}
                onClick={onOptimize}
            >
                Optimize Resume
            </Button>

        </Card>
    );
};

export default ResumeAnalysisCard;