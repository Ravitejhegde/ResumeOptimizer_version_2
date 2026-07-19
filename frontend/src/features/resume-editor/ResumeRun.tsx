import type { ResumeRun } from "./types";

type Props = {

    run: ResumeRun;

};

export default function ResumeRun({

    run,

}: Props) {

    return (

        <span

            style={{

                fontWeight: run.bold
                    ? 700
                    : 400,

                fontStyle: run.italic
                    ? "italic"
                    : "normal",

                textDecoration:
                    run.underline
                        ? "underline"
                        : "none",

                fontFamily:
                    run.fontName ??
                    "inherit",

                fontSize:
                    run.fontSize
                        ? `${run.fontSize}px`
                        : "inherit",

                color:
                    run.color
                        ? `#${run.color}`
                        : "inherit",

            }}

        >

            {run.text}

        </span>

    );

}