from app.services.intelligence.skills.skills_section_parser import (
    SkillsSectionParser,
)


class Paragraph:

    def __init__(self, text):

        self.text = text


def main():

    paragraphs = [

        Paragraph(
            "Frontend Technologies: Angular, TypeScript, JavaScript"
        ),

        Paragraph(
            "Backend Technologies: Python, FastAPI, REST APIs"
        ),

        Paragraph(
            "Database: PostgreSQL, MySQL"
        ),

        Paragraph(""),

    ]

    categories = SkillsSectionParser.parse(
        paragraphs
    )

    print()

    print("=" * 60)
    print("SKILLS SECTION PARSER")
    print("=" * 60)

    for category in categories:

        print(category.name)

        print(category.technologies)

        print()


if __name__ == "__main__":

    main()