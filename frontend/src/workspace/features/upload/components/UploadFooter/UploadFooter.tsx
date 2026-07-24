import styles from "./UploadFooter.module.css";

import type { UploadFooterProps } from "./UploadFooter.types";

const UploadFooter = ({
    maxSize = "5 MB",
    extension = ".docx"
}: UploadFooterProps) => {

    return (

        <div className={styles.footer}>

            <div className={styles.icon}>

                🛡️

            </div>

            <p>

                Only <strong>{extension}</strong> files.
                Maximum size <strong>{maxSize}</strong>

            </p>

        </div>

    );

};

export default UploadFooter;