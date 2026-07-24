import Card from "../../../../components/ui/Card/Card";

import styles from "./ExperienceCard.module.css";

import type { ExperienceCardProps } from "./ExperienceCard.types";

const ExperienceCard = ({
    years
}: ExperienceCardProps) => {

    return (

        <Card className={styles.card}>

            <span>

                Experience

            </span>

            <h4>

                {years}+ Years

            </h4>

        </Card>

    );

};

export default ExperienceCard;