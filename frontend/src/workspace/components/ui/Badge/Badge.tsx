import styles from "./Badge.module.css";

import type { BadgeProps } from "./Badge.types";

const Badge = ({
  children,
  variant = "neutral",
  className = "",
  ...props
}: BadgeProps) => {

  const classes = [
    styles.badge,
    styles[variant],
    className
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <span
      className={classes}
      {...props}
    >
      {children}
    </span>
  );

};

export default Badge;