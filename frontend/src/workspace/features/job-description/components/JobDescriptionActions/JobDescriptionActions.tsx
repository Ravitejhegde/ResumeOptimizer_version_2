import Button from "../../../../components/ui/Button/Button";

import styles from "./JobDescriptionActions.module.css";

import type { JobDescriptionActionsProps } from "./JobDescriptionActions.types";

const JobDescriptionActions = ({
    loading = false,
    disabled = false,
    onContinue
}: JobDescriptionActionsProps) => {

    return (

        <div className={styles.wrapper}>

            <div className={styles.info}>

                🔒 ResumeOptimizer never stores your resume permanently.

            </div>

            <Button
                size="lg"
                fullWidth
                loading={loading}
                disabled={disabled}
                onClick={onContinue}
            >

                Continue Analysis

            </Button>

        </div>

    );

};

export default JobDescriptionActions;