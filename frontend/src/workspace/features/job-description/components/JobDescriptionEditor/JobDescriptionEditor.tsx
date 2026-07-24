import Textarea from "../../../../components/ui/Textarea/Textarea";
import Button from "../../../../components/ui/Button/Button";

import styles from "./JobDescriptionEditor.module.css";

import type { JobDescriptionEditorProps } from "./JobDescriptionEditor.types";

const JobDescriptionEditor = ({
    value,
    maxLength = 5000,
    analyzed = false,
    onChange,
    onClear
}: JobDescriptionEditorProps) => {

    return (

        <div className={styles.wrapper}>

            <div className={styles.header}>

                <div className={styles.title}>

                    <span className={styles.step}>2</span>

                    <h3>Job Description</h3>

                </div>

                <span className={styles.counter}>

                    {value.length} / {maxLength}

                </span>

            </div>

            <Textarea

                value={value}

                placeholder="Paste the complete Job Description here..."

                onChange={(e) => onChange(e.target.value)}

            />

            <div className={styles.footer}>

                <Button
                    variant="outline"
                    onClick={onClear}
                >
                    Clear
                </Button>

                {analyzed && (

                    <div className={styles.status}>

                        ✓ JD Analyzed

                    </div>

                )}

            </div>

        </div>

    );

};

export default JobDescriptionEditor;