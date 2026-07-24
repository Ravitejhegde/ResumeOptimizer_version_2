import { useState } from "react";

import ResumePreview from "../ResumePreview/ResumePreview";

import { downloadResume } from "../../../../services/download/download.service";

import styles from "./DocumentViewer.module.css";

interface Props {

    blocks: any[];

    filename: string;

}

const DocumentViewer = ({

    blocks,

    filename,

}: Props) => {

    const [zoom, setZoom] = useState(100);

    const zoomIn = () => {

        setZoom(previous => Math.min(previous + 10, 200));

    };

    const zoomOut = () => {

        setZoom(previous => Math.max(previous - 10, 50));

    };

    return (

        <div className={styles.viewer}>

            <div className={styles.toolbar}>

                <button onClick={zoomOut}>
                    −
                </button>

                <span>
                    {zoom}%
                </span>

                <button onClick={zoomIn}>
                    +
                </button>

                <button
                    onClick={() => downloadResume(filename)}
                >
                    Download DOCX
                </button>

            </div>

            <div className={styles.canvas}>

                <div

                    style={{

                        transform: `scale(${zoom / 100})`,

                        transformOrigin: "top center",

                    }}

                >

                    <ResumePreview

                        blocks={blocks}

                    />

                </div>

            </div>

        </div>

    );

};

export default DocumentViewer;