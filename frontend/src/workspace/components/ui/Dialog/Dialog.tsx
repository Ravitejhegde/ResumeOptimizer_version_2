import styles from "./Dialog.module.css";

import type { DialogProps } from "./Dialog.types";

const Dialog = ({
  open,
  title,
  children,
  footer,
  onClose
}: DialogProps) => {

  if (!open) return null;

  return (

    <div
      className={styles.overlay}
      onClick={onClose}
    >

      <div
        className={styles.dialog}
        onClick={(e) => e.stopPropagation()}
      >

        {title && (

          <div className={styles.header}>

            {title}

          </div>

        )}

        <div className={styles.body}>

          {children}

        </div>

        {footer && (

          <div className={styles.footer}>

            {footer}

          </div>

        )}

      </div>

    </div>

  );

};

export default Dialog;