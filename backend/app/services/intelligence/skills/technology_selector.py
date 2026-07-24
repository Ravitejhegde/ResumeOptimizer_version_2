from app.services.intelligence.skills.technology_ranker import (
    TechnologyRanker,
)


class TechnologySelector:
    """
    Selects the highest-value technologies
    for the optimized Skills section.
    """

    @classmethod
    def select(
        cls,
        resume_categories,
        jd_skills,
        selected_skills,
        target_role,
        max_technologies=25,
    ):

        # -----------------------------------------
        # Flatten Resume Technologies
        # -----------------------------------------

        resume_skills = []

        for category in resume_categories:

            for technology in category.technologies:

                technology = technology.strip()

                if technology and technology not in resume_skills:

                    resume_skills.append(
                        technology
                    )

        # -----------------------------------------
        # Build Master Technology List
        # -----------------------------------------

        all_technologies = []

        for technology in resume_skills:

            if technology not in all_technologies:

                all_technologies.append(
                    technology
                )

        for technology in selected_skills:

            if technology not in all_technologies:

                all_technologies.append(
                    technology
                )

        for technology in jd_skills:

            if technology not in all_technologies:

                all_technologies.append(
                    technology
                )

        # -----------------------------------------
        # Rank Technologies
        # -----------------------------------------

        ranked = []

        for technology in all_technologies:

            score = TechnologyRanker.rank(

                technology=technology,

                target_role=target_role,

                resume_skills=resume_skills,

                jd_skills=jd_skills,

                selected_skills=selected_skills,

            )

            ranked.append(

                (
                    score,
                    technology,
                )

            )

        # -----------------------------------------
        # Highest Score First
        # -----------------------------------------

        ranked.sort(
            reverse=True
        )

        # -----------------------------------------
        # Apply Capacity
        # -----------------------------------------

        return [

            technology

            for score, technology in ranked[
                :max_technologies
            ]

        ]