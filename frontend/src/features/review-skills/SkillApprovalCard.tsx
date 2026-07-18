import styles from "./SkillApprovalCard.module.css";

type Props = {

    skills: string[];

    selected: string[];

    onToggle: (skill: string) => void;

};

export default function SkillApprovalCard({

    skills,

    selected,

    onToggle,

}: Props) {

    return (

        <div className={styles.container}>

            <h2 className={styles.title}>

                Review Suggested Skills

            </h2>

            <p className={styles.subtitle}>

                Select only the technologies you genuinely know.
                These will be added to your optimized resume.

            </p>

            <div className={styles.list}>

                {skills.map((skill) => (

                    <label

                        key={skill}

                        className={styles.item}

                    >

                        <input

                            className={styles.checkbox}

                            type="checkbox"

                            checked={selected.includes(skill)}

                            onChange={() =>
                                onToggle(skill)
                            }

                        />

                        <span className={styles.skill}>

                            {skill}

                        </span>

                    </label>

                ))}

            </div>

        </div>

    );

}