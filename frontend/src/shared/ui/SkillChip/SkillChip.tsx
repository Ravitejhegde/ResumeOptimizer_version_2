import styles from "./SkillChip.module.css";

type SkillChipProps = {
    label: string;
    matched: boolean;
};

export default function SkillChip({
    label,
    matched,
}: SkillChipProps) {
    return (
        <span
            className={`${styles.chip} ${
                matched ? styles.matched : styles.missing
            }`}
        >
            {matched ? "✓" : "•"} {label}
        </span>
    );
}