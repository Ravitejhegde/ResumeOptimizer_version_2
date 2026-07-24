import type { HTMLAttributes } from "react";

export interface ScoreRingProps
  extends HTMLAttributes<HTMLDivElement> {

  value: number;

  size?: number;

  strokeWidth?: number;

}