import styles from "./Chip.module.css";

import type { ChipProps } from "./Chip.types";

const Chip = ({
  children,
  variant = "default",
  selected = false,
  icon,
  className = "",
  ...props
}: ChipProps) => {

  const classes = [
    styles.chip,
    styles[variant],
    selected && styles.selected,
    className
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <button
      className={classes}
      type="button"
      {...props}
    >
      {icon}
      <span>{children}</span>
    </button>
  );
};

export default Chip;