export interface JobDescriptionEditorProps {

    value: string;

    maxLength?: number;

    analyzed?: boolean;

    onChange: (value: string) => void;

    onClear: () => void;

}