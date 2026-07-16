import { useRef } from "react";

import styles from "./UploadArea.module.css";

import { uploadResume } from "../../../services/analysisService";
import { useApp } from "../../../context/AppContext";

export default function UploadArea() {

    const inputRef =
        useRef<HTMLInputElement>(null);

    const {

        resume,
        setResume,

        setLoading,
        setError,
        setState,

    } = useApp();

    async function handleChange(

        event: React.ChangeEvent<HTMLInputElement>

    ) {

        const file =
            event.target.files?.[0];

        if (!file) {

            return;

        }

        try {

            setLoading(true);

            setError("");

            const result =
                await uploadResume(file);

            setResume(result);

            setState(
                "RESUME_UPLOADED"
            );

        }

        catch (error) {

            console.error(error);

            setError(
                "Failed to upload resume."
            );

        }

        finally {

            setLoading(false);

        }

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

                {

                    !resume ?

                        <>

                            <div className={styles.icon}>

                                📄

                            </div>

                            <h3>

                                Drag & Drop Resume

                            </h3>

                            <p>

                                or Browse Files

                            </p>

                            <span>

                                DOCX only • Max 5 MB

                            </span>

                        </>

                        :

                        <>

                            <div className={styles.success}>

                                ✅

                            </div>

                            <h3>

                                {resume.original_filename}

                            </h3>

                            <p>

                                Resume uploaded successfully

                            </p>

                            <button

                                type="button"

                                className={styles.change}

                                onClick={(e) => {

                                    e.stopPropagation();

                                    browse();

                                }}

                            >

                                Change File

                            </button>

                        </>

                }

            </div>

        </>

    );

}