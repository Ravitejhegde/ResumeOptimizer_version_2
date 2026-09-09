export interface ResumeAnalysisCardProps {

    score: number;

    role: string;

    experience: number;

    matchedTechnologies: string[];

    missingTechnologies: string[];

    selectedSkills: string[];

    onSkillToggle: (technology: string) => void;

    onSelectAll: () => void;

    onClearSelection: () => void;

    onOptimize: () => void;

    optimizing?: boolean;

}