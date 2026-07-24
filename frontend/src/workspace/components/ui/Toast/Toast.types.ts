import type { ReactNode } from "react";

export type ToastVariant =
    | "success"
    | "error"
    | "warning"
    | "info";

export interface ToastProps {

    open: boolean;

    title?: ReactNode;

    message: ReactNode;

    variant?: ToastVariant;

    duration?: number;

    onClose?: () => void;

}