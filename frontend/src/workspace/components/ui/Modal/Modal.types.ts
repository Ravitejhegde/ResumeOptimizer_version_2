import type { ReactNode } from "react";

export interface ModalProps {

  open: boolean;

  children: ReactNode;

  onClose: () => void;

}