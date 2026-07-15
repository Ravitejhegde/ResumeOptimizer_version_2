import styles from "./AnalysisScreen.module.css";

export default function AnalysisScreen() {

    return (

        <div className={styles.analysis}>

            <h2>
                Analyzing Resume...
            </h2>

            <ul>

                <li>✓ Reading Resume</li>

                <li>✓ Extracting Skills</li>

                <li>✓ Reading Job Description</li>

                <li>✓ Matching Keywords</li>

                <li>✓ Calculating Resume Match</li>

            </ul>

        </div>

    );

}