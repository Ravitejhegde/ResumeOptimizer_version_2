import type { ResumeBlock } from "./types";

import styles from "./ResumeEditor.module.css";

type Props = {

    block: ResumeBlock;

    onChange: (
        id: number,
        text: string,
    ) => void;

};

export default function EditableBlock({

    block,

    onChange,

}: Props) {

    return (

        <div className={styles.block}>

            <div className={styles.label}>

                {block.block_type}

            </div>

            <textarea

                className={styles.textarea}

                value={block.text}

                onChange={(e) =>

                    onChange(

                        block.id,

                        e.target.value,

                    )

                }

            />

        </div>

    );

}