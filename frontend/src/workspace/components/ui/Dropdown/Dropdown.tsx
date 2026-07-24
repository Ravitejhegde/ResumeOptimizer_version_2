import { useState } from "react";

import styles from "./Dropdown.module.css";

import type { DropdownProps } from "./Dropdown.types";

const Dropdown = ({
  options,
  value,
  placeholder = "Select",
  onChange,
  className = "",
  ...props
}: DropdownProps) => {

  const [open, setOpen] = useState(false);

  const selected =
    options.find(option => option.value === value);

  return (

    <div
      className={`${styles.dropdown} ${className}`}
      {...props}
    >

      <button
        type="button"
        className={styles.trigger}
        onClick={() => setOpen(!open)}
      >

        <span>

          {selected?.label ?? placeholder}

        </span>

        <span>▾</span>

      </button>

      {open && (

        <div className={styles.menu}>

          {options.map(option => (

            <button
              key={option.value}
              type="button"
              className={styles.item}
              onClick={() => {

                onChange?.(option.value);

                setOpen(false);

              }}
            >

              {option.label}

            </button>

          ))}

        </div>

      )}

    </div>

  );

};

export default Dropdown;