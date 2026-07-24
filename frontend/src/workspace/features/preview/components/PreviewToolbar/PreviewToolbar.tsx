import Button from "../../../../components/ui/Button/Button";

import styles from "./PreviewToolbar.module.css";

import type { PreviewToolbarProps } from "./PreviewToolbar.types";

const PreviewToolbar = ({
    onUndo,
    onRedo,
    onSave,
    saving = false
}: PreviewToolbarProps) => {

    return (

        <div className={styles.toolbar}>

            <Button
                variant="outline"
                onClick={onUndo}
            >
                Undo
            </Button>

            <Button
                variant="outline"
                onClick={onRedo}
            >
                Redo
            </Button>

            <Button
                loading={saving}
                onClick={onSave}
            >
                Save
            </Button>

        </div>

    );

};

export default PreviewToolbar;