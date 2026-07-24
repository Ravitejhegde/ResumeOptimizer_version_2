import DocumentViewer from "../../features/preview/components/DocumentViewer/DocumentViewer";

import { useWorkspace } from "../../store/useWorkspace";

import styles from "./OptimizationWorkspace.module.css";

const OptimizationWorkspace = () => {

    const { state } = useWorkspace();

    return (

        <div className={styles.workspace}>

            <h1>

                Optimized Resume

            </h1>

            <DocumentViewer
    blocks={state.previewBlocks}
    filename={state.optimizedFilename}
/>

        </div>

    );

};

export default OptimizationWorkspace;