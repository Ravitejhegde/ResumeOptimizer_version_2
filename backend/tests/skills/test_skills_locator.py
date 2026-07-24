from app.services.document.snapshot.snapshot_builder import (
    SnapshotBuilder,
)

from app.services.intelligence.skills.skills_section_locator import (
    SkillsSectionLocator,
)


def main():

    resume = (
        "tests/integration/input/resume.docx"
    )

    snapshot = SnapshotBuilder.build(
        resume
    )

    paragraphs = SkillsSectionLocator.locate(
        snapshot
    )

    print()

    print("=" * 60)
    print("SKILLS SECTION")
    print("=" * 60)

    if not paragraphs:

        print("Skills section not found.")
        return

    for paragraph in paragraphs:

        print(
            paragraph.id,
            "|",
            paragraph.text,
        )


if __name__ == "__main__":
    main()