import styles from "./Textarea.module.css";

import type { TextareaProps } from "./Textarea.types";

const Textarea = ({
  label,
  error,
  characterCount,
  maxCharacters,
  className = "",
  ...props
}: TextareaProps) => {

  return (

    <div className={styles.wrapper}>

      {label && (

        <label className={styles.label}>

          {label}

        </label>

      )}

      <textarea

        className={`${styles.textarea} ${className}`}

        {...props}

      />

      <div className={styles.footer}>

        {error ? (

          <span className={styles.error}>

            {error}

          </span>

        ) : (

          <span />

        )}

        {maxCharacters && (

          <span className={styles.counter}>

            {characterCount ?? 0}/{maxCharacters}

          </span>

        )}

      </div>

    </div>

  );

};

export default Textarea;