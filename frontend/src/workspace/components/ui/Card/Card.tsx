import styles from "./Card.module.css";
import type { CardProps } from "./Card.types";

const Card = ({
  children,
  className = "",
  ...props
}: CardProps) => {
  return (
    <div
      className={`${styles.card} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;