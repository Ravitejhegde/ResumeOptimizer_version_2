from __future__ import annotations

from dataclasses import dataclass, field



# ==================================================
# SKILL CATEGORY
# ==================================================

@dataclass(slots=True)
class JobSkillCategory:
    """
    JD skill grouping.

    Example:

    Machine Learning:
        TensorFlow
        PyTorch

    Cloud:
        AWS
        Docker
    """

    name: str = ""

    skills: list[str] = field(
        default_factory=list
    )




# ==================================================
# RESPONSIBILITY
# ==================================================

@dataclass(slots=True)
class JobResponsibility:
    """
    Represents JD responsibility area.
    """

    text: str = ""

    category: str = ""




# ==================================================
# JOB PROFILE
# ==================================================

@dataclass(slots=True)
class JobProfile:
    """
    Semantic understanding of Job Description.


    Created by:

        JobProfileAnalyzer


    Used by:

        SkillComparator
        IntelligenceEngine
        PromptBuilder


    Represents:

        "What company is looking for?"


    Does NOT:

        - Rewrite resume
        - Call AI
        - Modify DOCX
    """



    # ==================================================
    # ROLE INFORMATION
    # ==================================================

    title: str = ""


    role_family: str = ""


    seniority: str = ""



    # ==================================================
    # EXPERIENCE
    # ==================================================

    experience: str = ""


    years_required: str = ""



    # ==================================================
    # SKILLS
    # ==================================================

    skills: list[str] = field(
        default_factory=list
    )


    required_skills: list[str] = field(
        default_factory=list
    )


    preferred_skills: list[str] = field(
        default_factory=list
    )



    # ==================================================
    # TECHNOLOGY STACK
    # ==================================================

    technology_stack: list[str] = field(
        default_factory=list
    )



    # ==================================================
    # SKILL CATEGORIES
    # ==================================================

    skill_categories: list[
        JobSkillCategory
    ] = field(
        default_factory=list
    )



    # ==================================================
    # RESPONSIBILITIES
    # ==================================================

    responsibilities: list[
        JobResponsibility
    ] = field(
        default_factory=list
    )



    # ==================================================
    # DESCRIPTION THEME
    # ==================================================

    description_theme: list[str] = field(
        default_factory=list
    )



    # ==================================================
    # HELPERS
    # ==================================================

    @property
    def skill_count(
        self,
    ) -> int:

        return len(
            self.skills
        )



    @property
    def required_skill_count(
        self,
    ) -> int:

        return len(
            self.required_skills
        )



    @property
    def has_skills(
        self,
    ) -> bool:

        return bool(
            self.skills
        )



    def all_skills(
        self,
    ) -> list[str]:
        """
        Return unique skills
        from all sources.
        """

        result = set()


        result.update(
            self.skills
        )


        result.update(
            self.required_skills
        )


        result.update(
            self.preferred_skills
        )


        return sorted(
            result
        )



    def to_dict(
        self,
    ) -> dict:
        """
        Debug/API representation.
        """

        return {

            "title":
                self.title,


            "role_family":
                self.role_family,


            "seniority":
                self.seniority,


            "experience":
                self.experience,


            "skills":
                self.skills,


            "required_skills":
                self.required_skills,


            "preferred_skills":
                self.preferred_skills,


            "technology_stack":
                self.technology_stack,


            "skill_categories":
                [
                    {
                        "name": item.name,
                        "skills": item.skills
                    }

                    for item
                    in self.skill_categories
                ],


            "responsibilities":
                [
                    item.text
                    for item
                    in self.responsibilities
                ],


            "description_theme":
                self.description_theme,

        }