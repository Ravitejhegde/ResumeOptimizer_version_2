from __future__ import annotations

from dataclasses import dataclass, field



# ==================================================
# EXPERIENCE
# ==================================================

@dataclass(slots=True)
class Experience:
    """
    Professional experience information.

    Facts only.

    AI can improve wording,
    but cannot change these values.
    """


    company: str = ""

    role: str = ""

    duration: str = ""


    description: str = ""


    technologies: list[str] = field(
        default_factory=list
    )



# ==================================================
# EDUCATION
# ==================================================

@dataclass(slots=True)
class Education:
    """
    Education facts.

    Protected information.
    """


    degree: str = ""

    institution: str = ""

    year: str = ""

    grade: str = ""




# ==================================================
# PROJECT
# ==================================================

@dataclass(slots=True)
class Project:
    """
    Resume project representation.


    Used by AI optimization.


    Allowed:

        Improve description
        Improve keywords


    Forbidden:

        Invent project
        Invent technology
        Invent results
    """


    name: str = ""


    description: str = ""


    technologies: list[str] = field(
        default_factory=list
    )


    category: str = ""



# ==================================================
# SKILL CATEGORY
# ==================================================

@dataclass(slots=True)
class SkillCategory:
    """
    Group skills logically.

    Example:

    Programming:
        Python
        Java


    AI:
        YOLO
        OpenCV
    """


    name: str = ""


    skills: list[str] = field(
        default_factory=list
    )




# ==================================================
# RESUME PROFILE
# ==================================================

@dataclass(slots=True)
class ResumeProfile:
    """
    Complete semantic understanding
    of uploaded resume.


    This represents:

        "Who is this candidate?"


    It is created from:

        DOCX Reader
        Document Analyzer


    It is used by:

        Skill Comparator
        Intelligence Engine
        AI Prompt Builder


    Does NOT:

        - Modify DOCX
        - Rewrite content
        - Call AI
    """



    # ==================================================
    # PERSONAL INFORMATION
    # ==================================================

    name: str = ""

    email: str = ""

    phone: str = ""



    # ==================================================
    # PROFESSIONAL SUMMARY
    # ==================================================

    summary: str = ""



    # ==================================================
    # CURRENT POSITION
    # ==================================================

    current_role: str = ""



    target_roles: list[str] = field(
        default_factory=list
    )



    # ==================================================
    # SKILLS
    # ==================================================

    skills: list[str] = field(
        default_factory=list
    )


    skill_categories: list[
        SkillCategory
    ] = field(
        default_factory=list
    )



    # ==================================================
    # EXPERIENCE
    # ==================================================

    experience: list[
        Experience
    ] = field(
        default_factory=list
    )



    # ==================================================
    # EDUCATION
    # ==================================================

    education: list[
        Education
    ] = field(
        default_factory=list
    )



    # ==================================================
    # PROJECTS
    # ==================================================

    projects: list[
        Project
    ] = field(
        default_factory=list
    )



    # ==================================================
    # HELPERS
    # ==================================================

    @property
    def project_count(
        self,
    ) -> int:

        return len(
            self.projects
        )



    @property
    def experience_count(
        self,
    ) -> int:

        return len(
            self.experience
        )



    @property
    def all_technologies(
        self,
    ) -> list[str]:
        """
        Extract all technologies
        from projects and experience.
        """


        result = set()



        for project in self.projects:

            result.update(
                project.technologies
            )



        for exp in self.experience:

            result.update(
                exp.technologies
            )


        return sorted(
            result
        )



    @property
    def has_projects(
        self,
    ) -> bool:

        return bool(
            self.projects
        )



    def add_skill(
        self,
        skill: str,
    ) -> None:

        if skill and skill not in self.skills:

            self.skills.append(
                skill
            )



    def add_project(
        self,
        project: Project,
    ) -> None:

        self.projects.append(
            project
        )



    def to_dict(
        self,
    ) -> dict:
        """
        Debug/API representation.
        """


        return {


            "name":
                self.name,


            "current_role":
                self.current_role,


            "skills":
                self.skills,


            "skill_categories":
                [
                    {
                        "name": c.name,
                        "skills": c.skills
                    }

                    for c in self.skill_categories
                ],


            "projects":
                [
                    {
                        "name": p.name,
                        "technologies": p.technologies
                    }

                    for p in self.projects
                ],


            "experience_count":
                self.experience_count,


            "project_count":
                self.project_count,

        }