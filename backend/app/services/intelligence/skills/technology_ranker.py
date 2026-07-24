from app.services.intelligence.skills.technology_graph import (
    TECHNOLOGY_GRAPH,
)


class TechnologyRanker:
    """
    Scores technologies using the
    Technology Knowledge Graph.
    """

    @classmethod
    def rank(
        cls,
        technology: str,
        target_role: str,
        resume_skills: list[str],
        jd_skills: list[str],
        selected_skills: list[str],
    ) -> int:

        score = 0

        name = technology.strip()

        info = TECHNOLOGY_GRAPH.get(name)

        # -----------------------------------------
        # Base Priority
        # -----------------------------------------

        if info:

            score += info.priority

        else:

            score += 30

        # -----------------------------------------
        # Present in Resume
        # -----------------------------------------

        if name in resume_skills:

            score += 30

        # -----------------------------------------
        # Required by JD
        # -----------------------------------------

        if name in jd_skills:

            score += 50

        # -----------------------------------------
        # User Selected
        # -----------------------------------------

        if name in selected_skills:

            score += 70

        # -----------------------------------------
        # Matches Target Role
        # -----------------------------------------

        if info:

            if target_role in info.roles:

                score += 40

        # -----------------------------------------
        # Related Technologies Bonus
        # -----------------------------------------

        if info:

            for related in info.related:

                if related in jd_skills:

                    score += 10

        return score