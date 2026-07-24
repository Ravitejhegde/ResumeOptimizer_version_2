import type { ReactNode } from "react";

export interface DialogProps {

  open: boolean;

  title?: ReactNode;

  children: ReactNode;

  footer?: ReactNode;

  onClose: () => void;

}