export interface ParagraphBlockProps {

    id: string;

    text: string;

    editable: boolean;

    onEdit: (id: string, value: string) => void;

}