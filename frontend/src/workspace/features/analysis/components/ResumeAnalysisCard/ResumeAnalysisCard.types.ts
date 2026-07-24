export interface ResumeAnalysisCardProps {

    score: number;

    role: string;

    experience: number;

    matchedSkills: string[];

    missingSkills: string[];

    selectedSkills: string[];

    onSkillToggle: (skill: string) => void;

    onSelectAll: () => void;

    onClearSelection: () => void;

    onOptimize: () => void;

    optimizing?: boolean;

}