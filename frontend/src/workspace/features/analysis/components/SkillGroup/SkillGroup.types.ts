export interface SkillGroupProps {

    title: string;

    skills: string[];

    variant?: "success" | "danger";

    selectable?: boolean;

    selected?: string[];

    onToggle?: (skill: string) => void;

}