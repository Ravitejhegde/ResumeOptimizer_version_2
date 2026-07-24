import Card from "../../../../components/ui/Card/Card";
import ScoreRing from "../../../../components/ui/ScoreRing/ScoreRing";

import styles from "./ATSScoreCard.module.css";

import type { ATSScoreCardProps } from "./ATSScoreCard.types";

const ATSScoreCard = ({
    score,
    title = "ATS Score",
    subtitle = "Resume Match"
}: ATSScoreCardProps) => {

    return (

        <Card className={styles.card}>

            <h3>{title}</h3>

            <ScoreRing value={score} />

            <p>{subtitle}</p>

        </Card>

    );

};

export default ATSScoreCard;