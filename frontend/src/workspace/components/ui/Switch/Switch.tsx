import styles from "./Switch.module.css";

import type { SwitchProps } from "./Switch.types";

const Switch = ({
  label,
  className = "",
  ...props
}: SwitchProps) => {

  return (

    <label className={`${styles.switch} ${className}`}>

      <input
        type="checkbox"
        {...props}
      />

      <span className={styles.slider}></span>

      {label && (

        <span className={styles.label}>

          {label}

        </span>

      )}

    </label>

  );

};

export default Switch;