import Button from "../../../../components/ui/Button/Button";

import styles from "./UploadedResumeCard.module.css";

import type { UploadedResumeCardProps } from "./UploadedResumeCard.types";

const UploadedResumeCard = ({
    filename,
    fileSize,
    uploaded = true,
    onReplace,
    onRemove
}: UploadedResumeCardProps) => {

    return (

        <div className={styles.card}>

            <div className={styles.left}>

                <div className={styles.icon}>

                    DOCX

                </div>

                <div>

                    <h4>

                        {filename}

                    </h4>

                    <span>

                        {fileSize}

                    </span>

                </div>

            </div>

            <div className={styles.right}>

                {uploaded &&

                    <div className={styles.success}>

                        ✓

                    </div>

                }

                <Button
                    variant="ghost"
                    size="sm"
                    onClick={onReplace}
                >

                    Replace

                </Button>

                <Button
                    variant="ghost"
                    size="sm"
                    onClick={onRemove}
                >

                    Remove

                </Button>

            </div>

        </div>

    );

};

export default UploadedResumeCard;