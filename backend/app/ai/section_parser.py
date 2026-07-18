import re

SECTION_HEADERS = [
    "SUMMARY",
    "PROFILE",
    "EXPERIENCE",
    "WORK EXPERIENCE",
    "EMPLOYMENT",
    "PROJECTS",
    "PROJECT",
    "SKILLS",
    "TECHNICAL SKILLS",
    "EDUCATION",
    "CERTIFICATIONS",
    "ACHIEVEMENTS",
    "LANGUAGES",
]


def split_sections(text: str):

    lines = text.splitlines()

    sections = []

    current_title = "GENERAL"

    current_content = []

    for line in lines:

        clean = line.strip()

        if not clean:
            continue

        upper = clean.upper()

        if upper in SECTION_HEADERS:

            sections.append(
                (
                    current_title,
                    "\n".join(current_content),
                )
            )

            current_title = clean

            current_content = []

        else:

            current_content.append(clean)

    sections.append(

        (
            current_title,
            "\n".join(current_content),
        )

    )

    return sections