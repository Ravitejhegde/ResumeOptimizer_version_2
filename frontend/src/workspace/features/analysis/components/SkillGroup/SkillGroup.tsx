import Chip from "../../../../components/ui/Chip/Chip";

import styles from "./SkillGroup.module.css";

import type { SkillGroupProps } from "./SkillGroup.types";

const SkillGroup = ({
    title,
    skills,
    variant = "success",
    selectable = false,
    selected = [],
    onToggle
}: SkillGroupProps) => {

    return (

        <div className={styles.group}>

            <h4>

                {title}

            </h4>

            <div className={styles.skills}>

                {skills.map(skill => (

                    <Chip
                        key={skill}
                        variant={variant}
                        selected={selected.includes(skill)}
                        onClick={() => selectable && onToggle?.(skill)}
                    >

                        {skill}

                    </Chip>

                ))}

            </div>

        </div>

    );

};

export default SkillGroup;