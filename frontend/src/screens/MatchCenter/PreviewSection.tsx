import ResumeEditor from "../../features/resume-editor/ResumeEditor";

import PrimaryButton from "../../shared/ui/Button/PrimaryButton";

import {
    downloadResume as downloadResumeApi,
} from "../../services/downloadApi";

import type { ResumeBlock } from "../../features/resume-editor/types";

type Props = {

    optimizedFilename: string;

    previewBlocks: ResumeBlock[];

    setPreviewBlocks: React.Dispatch<
        React.SetStateAction<ResumeBlock[]>
    >;

};

export default function PreviewSection({

    optimizedFilename,

    previewBlocks,

    setPreviewBlocks,

}: Props) {

    async function downloadResume() {

        if (!optimizedFilename) {

            alert(
                "Please optimize the resume first."
            );

            return;

        }

        try {

            const response =
                await downloadResumeApi(
                    optimizedFilename,
                );

            const blob = new Blob(

                [response.data],

                {

                    type:
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",

                },

            );

            const url =
                window.URL.createObjectURL(
                    blob,
                );

            const link =
                document.createElement("a");

            link.href = url;

            link.download =
                optimizedFilename;

            link.click();

            window.URL.revokeObjectURL(
                url,
            );

        }

        catch (error) {

            console.error(error);

            alert(
                "Download failed."
            );

        }

    }

    return (

        <>

            <ResumeEditor

                blocks={previewBlocks}

                onBlocksChange={
                    setPreviewBlocks
                }

            />

            <div style={{ height: 24 }} />

            <PrimaryButton

                title="Download Optimized Resume"

                onClick={
                    downloadResume
                }

            />

        </>

    );

}