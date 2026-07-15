import styles from "./MatchCenterScreen.module.css";

import SkillChip from "../../shared/ui/SkillChip/SkillChip";

export default function MatchCenterScreen() {

    return (

        <main className={styles.page}>

            <div className={styles.card}>

                <h1>Resume Match</h1>

                <div className={styles.score}>

                    87%

                </div>

                <div className={styles.progress}>

                    <div className={styles.fill}></div>

                </div>

                <p className={styles.status}>
                    Excellent Match
                </p>

                <section>

                    <h2>Matched Skills</h2>

                    <div className={styles.skills}>

                        <SkillChip
                            label="React"
                            matched={true}
                        />

                        <SkillChip
                            label="REST API"
                            matched={true}
                        />

                        <SkillChip
                            label="Git"
                            matched={true}
                        />

                        <SkillChip
                            label="JavaScript"
                            matched={true}
                        />

                    </div>

                </section>

                <section>

                    <h2>Missing Skills</h2>

                    <div className={styles.skills}>

                        <SkillChip
                            label="Docker"
                            matched={false}
                        />

                        <SkillChip
                            label="AWS"
                            matched={false}
                        />

                        <SkillChip
                            label="CI/CD"
                            matched={false}
                        />

                        <SkillChip
                            label="Kubernetes"
                            matched={false}
                        />

                    </div>

                </section>

                <section>

                    <h2>AI Suggestions</h2>

                    <ul className={styles.list}>

                        <li>
                            Mention Docker experience.
                        </li>

                        <li>
                            Highlight REST API scalability.
                        </li>

                        <li>
                            Add CI/CD knowledge.
                        </li>

                    </ul>

                </section>

                <section>

                    <h2>Recruiter View</h2>

                    <ul className={styles.list}>

                        <li>
                            Strong React profile.
                        </li>

                        <li>
                            Good backend experience.
                        </li>

                        <li>
                            Cloud experience should be highlighted.
                        </li>

                    </ul>

                </section>

            </div>

        </main>

    );

}