from app.document.parser.snapshot_builder import SnapshotBuilder
from app.document.parser.block_builder import BlockBuilder

from app.services.intelligence.engine import (
    ResumeIntelligenceEngine,
)


def test_engine():

    resume_path = "storage/temp/test.docx"

    snapshot = SnapshotBuilder.build(
        resume_path,
    )

    blocks = BlockBuilder.build(
        snapshot,
    )

    job_description = """

Responsibilities

Develop Full Stack applications.

React

Angular

Vue

Node.js

Git

REST API

SQL

CI/CD

"""

    engine = ResumeIntelligenceEngine()

    plan = engine.build_plan(

        blocks=blocks,

        job_description=job_description,

        selected_skills=[],

    )

    print()

    print(plan)

    print()


if __name__ == "__main__":

    test_engine()