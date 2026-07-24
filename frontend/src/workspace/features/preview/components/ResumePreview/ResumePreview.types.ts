export interface ParagraphBlock {

    id: string;

    text: string;

    editable: boolean;

}

export interface ResumePreviewProps {

    blocks: ParagraphBlock[];

    onEdit: (id: string, value: string) => void;

}