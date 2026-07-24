import styles from "./Modal.module.css";

import type { ModalProps } from "./Modal.types";

const Modal = ({
  open,
  children,
  onClose
}: ModalProps) => {

  if (!open) return null;

  return (

    <div
      className={styles.overlay}
      onClick={onClose}
    >

      <div
        className={styles.modal}
        onClick={(event) => event.stopPropagation()}
      >

        {children}

      </div>

    </div>

  );

};

export default Modal;