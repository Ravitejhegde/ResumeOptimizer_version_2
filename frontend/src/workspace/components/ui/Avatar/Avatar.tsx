import styles from "./Avatar.module.css";

import type { AvatarProps } from "./Avatar.types";

const Avatar = ({
  src,
  alt = "Avatar",
  initials = "U",
  size = "md",
  className = "",
  ...props
}: AvatarProps) => {

  const classes = [
    styles.avatar,
    styles[size],
    className
  ]
    .filter(Boolean)
    .join(" ");

  return (

    <div
      className={classes}
      {...props}
    >

      {src ? (

        <img
          src={src}
          alt={alt}
        />

      ) : (

        <span>

          {initials}

        </span>

      )}

    </div>

  );

};

export default Avatar;