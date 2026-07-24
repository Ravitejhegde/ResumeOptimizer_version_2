import styles from "./Spinner.module.css";

import type { SpinnerProps } from "./Spinner.types";

const Spinner = ({
  size = "md",
  className = "",
  ...props
}: SpinnerProps) => {

  const classes = [
    styles.spinner,
    styles[size],
    className
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <div
      className={classes}
      aria-label="Loading"
      role="status"
      {...props}
    />
  );

};

export default Spinner;