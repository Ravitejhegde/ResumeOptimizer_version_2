import styles from "./ResumePreview.module.css";

type Props = {

    previewUrl?: string;

};

export default function ResumePreview({

    previewUrl,

}: Props) {

    return (

        <div className={styles.container}>

            <h2 className={styles.title}>

                Resume Preview

            </h2>

            <div className={styles.paper}>

                {previewUrl ? (

                    <iframe

                        src={previewUrl}

                        title="Resume Preview"

                        width="100%"

                        height="100%"

                        style={{
                            border: "none",
                        }}

                    />

                ) : (

                    <div className={styles.placeholder}>

                        <div className={styles.icon}>

                            📄

                        </div>

                        <div className={styles.text}>

                            Preview will appear here

                        </div>

                        <div className={styles.subtext}>

                            After optimization your resume
                            will be displayed here.

                        </div>

                    </div>

                )}

            </div>

        </div>

    );

}