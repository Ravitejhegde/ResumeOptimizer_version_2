export interface UploadedResumeCardProps {

    filename: string;

    fileSize: string;

    uploaded?: boolean;

    onReplace?: () => void;

    onRemove?: () => void;

}