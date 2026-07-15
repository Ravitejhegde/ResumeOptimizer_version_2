import styles from "../../app/App.module.css";

import Container from "../../shared/ui/Container/Container";
import Card from "../../shared/ui/Card/Card";
import UploadArea from "../../shared/ui/UploadArea/UploadArea";
import Button from "../../shared/ui/Button/Button";
import JobDescriptionAnalyzer from "../../features/job-description/JobDescriptionAnalyzer";

export default function EmptyScreen() {
    return (
        <main className={styles.page}>
            <Container>
                <Card>

                    <div className={styles.hero}>
                        <h1 className={styles.title}>
                            ResumeOptimizer
                        </h1>

                        <p className={styles.subtitle}>
                            Same Resume. Smarter Words.
                        </p>
                    </div>

                    <UploadArea />

                    <br />

                    <JobDescriptionAnalyzer />

                    <br />

                    <Button>
                        Analyze Resume
                    </Button>

                </Card>
            </Container>
        </main>
    );
}