import type { HTMLAttributes, ReactNode } from "react";

export type BadgeVariant =
  | "primary"
  | "success"
  | "warning"
  | "danger"
  | "neutral";

export interface BadgeProps
  extends HTMLAttributes<HTMLSpanElement> {

  variant?: BadgeVariant;

  children: ReactNode;

}