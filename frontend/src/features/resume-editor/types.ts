export interface ResumeRun {

    text: string;

    bold: boolean;

    italic: boolean;

    underline: boolean;

    fontName?: string;

    fontSize?: number;

    color?: string;

}

export interface ResumeBlock {

    id: number;

    paragraphIndex: number;

    text: string;

    style: string;

    blockType: string;

    editable: boolean;

    modified?: boolean;

    section: string;

    runs: ResumeRun[];

}

export interface ResumeParagraph {

    id: number;

    paragraphIndex: number;

    text: string;

    style: string;

    blockType: string;

    editable: boolean;

    section: string;

    runs: ResumeRun[];

}