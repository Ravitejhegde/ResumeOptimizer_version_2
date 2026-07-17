import { useRef } from "react";

import styles from "./UploadCard.module.css";

type Props = {
    file: File | null;
    onFileSelect: (file: File) => void;
};

export default function UploadCard({
    file,
    onFileSelect,
}: Props) {

    const inputRef =
        useRef<HTMLInputElement>(null);

    function openPicker() {

        inputRef.current?.click();

    }

    function handleChange(
        e: React.ChangeEvent<HTMLInputElement>
    ) {

        const selected =
            e.target.files?.[0];

        if (!selected) return;

        onFileSelect(selected);

    }

    return (

        <div className={styles.container}>

            <h2 className={styles.title}>

                Upload Resume

            </h2>

            <div className={styles.dropArea}>

                <div className={styles.icon}>

                    📄

                </div>

                <p className={styles.subtitle}>

                    Drag & Drop your DOCX resume

                </p>

                <button

                    className={styles.button}

                    onClick={openPicker}

                >

                    Choose Resume

                </button>

                <input

                    hidden

                    ref={inputRef}

                    type="file"

                    accept=".docx"

                    onChange={handleChange}

                />

            </div>

            {file && (

                <div className={styles.fileInfo}>

                    <span>

                        {file.name}

                    </span>

                    <span className={styles.success}>

                        ✓ Uploaded

                    </span>

                </div>

            )}

        </div>

    );

}