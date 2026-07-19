import { useEffect, useState } from "react";

import type { ResumeBlock } from "./types";

import EditableBlock from "./EditableBlock";

import styles from "./ResumeEditor.module.css";

type Props = {

    blocks: ResumeBlock[];

    onBlocksChange: (
        blocks: ResumeBlock[],
    ) => void;

};

export default function ResumeEditor({

    blocks,

    onBlocksChange,

}: Props) {

    const [

        editorBlocks,

        setEditorBlocks,

    ] = useState<ResumeBlock[]>([]);

    useEffect(() => {

        setEditorBlocks(blocks ?? []);

    }, [blocks]);

    function updateBlock(

        id: number,

        text: string,

    ) {

        const updated = (editorBlocks ?? []).map(

            block =>

                block.id === id

                    ? {

                          ...block,

                          text,

                          modified: true,

                      }

                    : block

        );

        setEditorBlocks(updated);

        onBlocksChange(updated);

    }

    return (

        <div className={styles.container}>

            <div className={styles.heading}>

                Resume Preview

            </div>

            <div className={styles.paper}>

                {(editorBlocks ?? []).map(

                    block => (

                        <EditableBlock

                            key={block.id}

                            block={block}

                            onChange={updateBlock}

                        />

                    )

                )}

            </div>

        </div>

    );

}