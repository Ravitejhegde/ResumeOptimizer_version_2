import styles from "./JobDescriptionCard.module.css";

type Props = {

    value: string;

    onChange: (
        value: string,
    ) => void;

};

const MAX_LENGTH = 5000;

export default function JobDescriptionCard({

    value,

    onChange,

}: Props) {

    return (

        <div className={styles.container}>

            <h2 className={styles.title}>

                Job Description

            </h2>

            <textarea

                className={styles.textarea}

                placeholder="Paste the complete job description here..."

                value={value}

                maxLength={MAX_LENGTH}

                onChange={(e) =>

                    onChange(
                        e.target.value,
                    )

                }

            />

            <div className={styles.footer}>

                <span className={styles.counter}>

                    {value.length} / {MAX_LENGTH}

                </span>

            </div>

        </div>

    );

}