import { useRef, useState } from "react";

import Button from "../../../../components/ui/Button/Button";

import { uploadResume } from "../../../../services/upload/upload.service";

import { useWorkspace } from "../../../../store/useWorkspace";

import styles from "./UploadDropzone.module.css";

import type { UploadDropzoneProps } from "./UploadDropzone.types";

const MAX_FILE_SIZE = 5 * 1024 * 1024;

const UploadDropzone = ({
    onBrowse,
    onDrop
}: UploadDropzoneProps) => {

    const inputRef = useRef<HTMLInputElement>(null);

    const [dragging, setDragging] = useState(false);

    const [loading, setLoading] = useState(false);

    const {
        setState
    } = useWorkspace();

    const upload = async (file: File) => {

        try {

            setLoading(true);

            const response = await uploadResume(file);

            setState(previous => ({

                ...previous,

                resume: {

                    id: response.resume_id,

                    filename: response.filename,

                    storedFilename: response.stored_filename

                }

            }));

        }

        catch (error: any) {

            console.error(error);

            console.log(error.response);

            console.log(error.response?.data);

            alert(

                error.response?.data?.detail ??

                error.message ??

                "Resume upload failed."

            );

        }

        finally {

            setLoading(false);

        }

    };

    const validate = (file: File) => {

        if (!file.name.toLowerCase().endsWith(".docx")) {

            alert("Only DOCX files are allowed.");

            return false;

        }

        if (file.size > MAX_FILE_SIZE) {

            alert("Maximum size is 5 MB.");

            return false;

        }

        return true;

    };

    const handleFiles = async (

        files: FileList | null

    ) => {

        if (!files?.length) {

            return;

        }

        const file = files[0];

        if (!validate(file)) {

            return;

        }

        await upload(file);

        onDrop(files);

    };

    return (

        <div

            className={`${styles.dropzone} ${dragging ? styles.active : ""}`}

            onDragOver={(event) => {

                event.preventDefault();

                setDragging(true);

            }}

            onDragLeave={() => {

                setDragging(false);

            }}

            onDrop={(event) => {

                event.preventDefault();

                setDragging(false);

                handleFiles(event.dataTransfer.files);

            }}

        >

            <input

                hidden

                ref={inputRef}

                type="file"

                accept=".docx"

                onChange={(event) =>

                    handleFiles(event.target.files)

                }

            />

            <div className={styles.icon}>

                📄

            </div>

            <h3>

                Upload Resume

            </h3>

            <p>

                Drag & Drop DOCX here

            </p>

            <Button

                size="lg"

                loading={loading}

                onClick={() => {

                    inputRef.current?.click();

                    onBrowse();

                }}

            >

                Browse Resume

            </Button>

            <span className={styles.note}>

                DOCX • Max 5 MB

            </span>

        </div>

    );

};

export default UploadDropzone;