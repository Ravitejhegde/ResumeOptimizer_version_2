import styles from "./Tooltip.module.css";

import type { TooltipProps } from "./Tooltip.types";

const Tooltip = ({
    content,
    children,
    position = "top"
}: TooltipProps) => {

    return (

        <div className={styles.wrapper}>

            {children}

            <div className={`${styles.tooltip} ${styles[position]}`}>

                {content}

            </div>

        </div>

    );

};

export default Tooltip;