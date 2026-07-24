import type { ReactNode } from "react";

export interface DropdownOption {
  label: string;
  value: string;
  icon?: ReactNode;
  disabled?: boolean;
}

export interface DropdownProps {
  value?: string;

  placeholder?: string;

  options: DropdownOption[];

  onChange?: (value: string) => void;

  className?: string;

  disabled?: boolean;
}