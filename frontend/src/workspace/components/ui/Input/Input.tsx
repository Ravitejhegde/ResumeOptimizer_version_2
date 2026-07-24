import styles from "./Input.module.css";

import type { InputProps } from "./Input.types";

const Input = ({
  label,
  error,
  className = "",
  ...props
}: InputProps) => {

  return (

    <div className={styles.wrapper}>

      {label && (

        <label className={styles.label}>

          {label}

        </label>

      )}

      <input

        className={`${styles.input} ${className}`}

        {...props}

      />

      {error && (

        <p className={styles.error}>

          {error}

        </p>

      )}

    </div>

  );

};

export default Input;