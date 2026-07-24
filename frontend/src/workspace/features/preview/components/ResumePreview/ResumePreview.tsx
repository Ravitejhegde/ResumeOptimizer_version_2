import styles from "./ResumePreview.module.css";

interface ResumeRun {

    text: string;

    bold?: boolean;

    italic?: boolean;

    underline?: boolean;

    fontName?: string;

    fontSize?: number;

    color?: string;

}

interface ResumeBlock {

    id: number | string;

    text: string;

    runs?: ResumeRun[];

}

interface Props {

    blocks: ResumeBlock[];

}

const ResumePreview = ({ blocks }: Props) => {

    return (

        <div className={styles.paper}>

            {blocks.map((block) => (

                <p
                    key={block.id}
                    className={styles.paragraph}
                >

                    {block.runs && block.runs.length > 0 ? (

                        block.runs.map((run, index) => (

                            <span
                                key={index}
                                style={{

                                    fontWeight: run.bold
                                        ? 700
                                        : 400,

                                    fontStyle: run.italic
                                        ? "italic"
                                        : "normal",

                                    textDecoration: run.underline
                                        ? "underline"
                                        : "none",

                                    fontFamily:
                                        run.fontName,

                                    fontSize: run.fontSize
                                        ? `${run.fontSize}px`
                                        : undefined,

                                    color:
                                        run.color || undefined,

                                }}
                            >

                                {run.text}

                            </span>

                        ))

                    ) : (

                        block.text

                    )}

                </p>

            ))}

        </div>

    );

};

export default ResumePreview;