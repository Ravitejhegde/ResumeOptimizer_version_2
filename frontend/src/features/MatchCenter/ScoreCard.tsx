type Props = {

    score: number;

};

export default function ScoreCard({

    score,

}: Props) {

    return (

        <div className="score-card">

            <h3>

                Overall Match Score

            </h3>

            <div className="score-value">

                {score}%

            </div>

        </div>

    );

}