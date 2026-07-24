import type { ButtonHTMLAttributes, ReactNode } from "react";

export type ChipVariant =
  | "default"
  | "success"
  | "danger"
  | "primary";

export interface ChipProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {

  variant?: ChipVariant;

  selected?: boolean;

  icon?: ReactNode;

  children: ReactNode;

}