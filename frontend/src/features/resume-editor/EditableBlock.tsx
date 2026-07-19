import { useEffect, useState } from "react";

import type { ResumeBlock } from "./types";
import ResumeRun from "./ResumeRun";
import styles from "./ResumeEditor.module.css";
import { getStyleClass } from "./styleMapper";

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

    const [editing, setEditing] =
        useState(false);

    const [text, setText] =
        useState(block.text);

    useEffect(() => {

        setText(block.text);

    }, [block.text]);

    function save() {

        onChange(
            block.id,
            text,
        );

        setEditing(false);

    }
    const isHeading =
    block.style.toLowerCase().includes("heading");

const isTitle =
    block.style.toLowerCase().includes("title");
    return (

        <div
    className={`${styles.block}
    ${isHeading ? styles.headingSpacing : ""}
    ${isTitle ? styles.titleSpacing : ""}`}
>

            {!editing ? (

                <div
    className={`${styles.preview} ${
        styles[getStyleClass(block.style) as keyof typeof styles] || ""
    }`}
    onClick={() => setEditing(true)}
>

    {block.runs.length > 0 ? (

    block.runs.map(

        (run, index) => (

            <ResumeRun

                key={index}

                run={run}

            />

        )

    )

) : (

    text || "Click to edit..."

)}

    {block.modified && (

        <span className={styles.badge}>

            Edited

        </span>

    )}

</div>

            ) : (

                <textarea

                    autoFocus

                    className={styles.textarea}

                    value={text}

                    onChange={(e) =>
                        setText(
                            e.target.value
                        )
                    }

                    onBlur={save}

                />

            )}

        </div>

    );

}