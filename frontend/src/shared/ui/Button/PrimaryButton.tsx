import styles from "./PrimaryButton.module.css";

type Props = {

    title: string;

    disabled?: boolean;

    onClick: () => void;

};

export default function PrimaryButton({

    title,

    disabled,

    onClick,

}: Props) {

    return (

        <button

            className={styles.button}

            disabled={disabled}

            onClick={onClick}

        >

            {title}

        </button>

    );

}