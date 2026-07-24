import styles from "./Button.module.css";

import type { ButtonProps } from "./Button.types";

const Button = ({
  children,
  variant = "primary",
  size = "md",
  fullWidth = false,
  loading = false,
  leftIcon,
  rightIcon,
  className = "",
  disabled,
  ...props
}: ButtonProps) => {

  const classes = [

    styles.button,

    styles[variant],

    styles[size],

    fullWidth && styles.fullWidth,

    loading && styles.loading,

    className

  ]
    .filter(Boolean)
    .join(" ");

  return (

    <button

      className={classes}

      disabled={disabled || loading}

      {...props}

    >

      {loading ? (

        <span className={styles.spinner} />

      ) : (

        <>
          {leftIcon}

          <span>{children}</span>

          {rightIcon}
        </>

      )}

    </button>

  );

};

export default Button;