import styles from "./ParagraphBlock.module.css";

import type { ParagraphBlockProps } from "./ParagraphBlock.types";

const ParagraphBlock = ({
    id,
    text,
    editable,
    onEdit
}: ParagraphBlockProps) => {

    if (!editable) {

        return (

            <p className={styles.readonly}>

                {text}

            </p>

        );

    }

    return (

        <div
            className={styles.editable}
            contentEditable
            suppressContentEditableWarning
            onBlur={(event) =>
                onEdit(id, event.currentTarget.innerText)
            }
        >

            {text}

        </div>

    );

};

export default ParagraphBlock;