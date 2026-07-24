import { useEffect } from "react";

import styles from "./Toast.module.css";

import type { ToastProps } from "./Toast.types";

const Toast = ({
    open,
    title,
    message,
    variant = "info",
    duration = 3000,
    onClose
}: ToastProps) => {

    useEffect(() => {

        if (!open) return;

        const timer = window.setTimeout(() => {

            onClose?.();

        }, duration);

        return () => window.clearTimeout(timer);

    }, [open, duration, onClose]);

    if (!open) return null;

    return (

        <div className={`${styles.toast} ${styles[variant]}`}>

            {title && (

                <h4>{title}</h4>

            )}

            <p>{message}</p>

        </div>

    );

};

export default Toast;