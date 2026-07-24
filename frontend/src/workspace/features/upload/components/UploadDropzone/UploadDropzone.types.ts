export interface UploadDropzoneProps {

    file?: File | null;

    loading?: boolean;

    onBrowse: () => void;

    onDrop: (files: FileList) => void;

}