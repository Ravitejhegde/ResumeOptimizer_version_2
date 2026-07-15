import { useRef, useState } from "react";
import styles from "./UploadArea.module.css";

export default function UploadArea() {
    const inputRef = useRef<HTMLInputElement>(null);

    const [file, setFile] = useState<File | null>(null);

    function handleChange(
        event: React.ChangeEvent<HTMLInputElement>
    ) {
        const selected = event.target.files?.[0];

        if (!selected) return;

        setFile(selected);
    }

    function browse() {
        inputRef.current?.click();
    }

    return (
        <>
            <input
                ref={inputRef}
                type="file"
                accept=".docx"
                hidden
                onChange={handleChange}
            />

            <div
                className={styles.upload}
                onClick={browse}
            >
                {!file ? (
                    <>
                        <div className={styles.icon}>
                            📄
                        </div>

                        <h3>Drag & Drop Resume</h3>

                        <p>or Browse Files</p>

                        <span>
                            DOCX only • Max 5 MB
                        </span>
                    </>
                ) : (
                    <>
                        <div className={styles.success}>
                            ✅
                        </div>

                        <h3>{file.name}</h3>

                        <p>
                            {(file.size / 1024).toFixed(1)} KB
                        </p>

                        <button
                            className={styles.change}
                        >
                            Change File
                        </button>
                    </>
                )}
            </div>
        </>
    );
}