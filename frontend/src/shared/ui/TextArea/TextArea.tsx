import styles from "./TextArea.module.css";

import type { TextareaHTMLAttributes } from "react";

type TextAreaProps =
    TextareaHTMLAttributes<HTMLTextAreaElement>;

export default function TextArea(
    props: TextAreaProps
) {
    return (
        <textarea
            className={styles.textarea}
            {...props}
        />
    );
}