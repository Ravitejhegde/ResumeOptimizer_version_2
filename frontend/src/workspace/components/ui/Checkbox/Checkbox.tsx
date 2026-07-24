import styles from "./Checkbox.module.css";

import type { CheckboxProps } from "./Checkbox.types";

const Checkbox = ({
  label,
  className = "",
  ...props
}: CheckboxProps) => {

  return (

    <label className={`${styles.checkbox} ${className}`}>

      <input
        type="checkbox"
        {...props}
      />

      <span className={styles.box}></span>

      {label && (

        <span className={styles.label}>

          {label}

        </span>

      )}

    </label>

  );

};

export default Checkbox;