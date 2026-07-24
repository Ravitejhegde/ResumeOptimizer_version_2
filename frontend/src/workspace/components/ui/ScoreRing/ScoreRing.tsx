import styles from "./ScoreRing.module.css";

import type { ScoreRingProps } from "./ScoreRing.types";

const ScoreRing = ({
  value,
  size = 120,
  strokeWidth = 10,
  className = "",
  ...props
}: ScoreRingProps) => {

  const radius = (size - strokeWidth) / 2;

  const circumference = 2 * Math.PI * radius;

  const offset =
    circumference - (value / 100) * circumference;

  return (

    <div
      className={`${styles.wrapper} ${className}`}
      {...props}
    >

      <svg
        width={size}
        height={size}
      >

        <circle
          className={styles.track}
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
        />

        <circle
          className={styles.progress}
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
        />

      </svg>

      <div className={styles.center}>

        <h2>{value}</h2>

        <span>ATS</span>

      </div>

    </div>

  );

};

export default ScoreRing;