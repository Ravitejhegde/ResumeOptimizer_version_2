from app.services.intelligence.models import (
    ResumeAnalysis,
    Skill,
)


class SectionMapper:
    """
    Decides where a technology should be placed
    inside the resume.
    """

    DEFAULT_SECTIONS = {

        "Programming Languages":
            "Programming Languages",

        "Frontend Technologies":
            "Frontend Technologies",

        "Backend Technologies":
            "Backend Technologies",

        "Databases":
            "Databases",

        "Frameworks":
            "Frameworks",

        "Cloud":
            "Cloud",

        "DevOps":
            "DevOps",

        "Testing":
            "Testing",

        "Tools & Platforms":
            "Tools & Platforms",

        "Mobile":
            "Mobile",

        "Artificial Intelligence":
            "Artificial Intelligence",

        "Soft Skills":
            "Soft Skills",

        "Other":
            "Other",

    }

    @staticmethod
    def find_section(

        resume: ResumeAnalysis,

        skill: Skill,

    ) -> str:

        # ---------------------------------------
        # Existing section already present
        # ---------------------------------------

        for section in resume.sections:

            if section.name.lower() == skill.section.lower():

                return section.name

        # ---------------------------------------
        # Match by category
        # ---------------------------------------

        section_name = SectionMapper.DEFAULT_SECTIONS.get(

            skill.category.value,

            "Other",

        )

        for section in resume.sections:

            if section.name.lower() == section_name.lower():

                return section.name

        # ---------------------------------------
        # Section doesn't exist
        # ---------------------------------------

        return section_name