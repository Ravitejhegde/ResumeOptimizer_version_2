from app.services.intelligence.models import (
    SkillDecision,
    SkillAction,
)


class ReplacementEngine:

    @staticmethod
    def build(

        keep: list[SkillDecision],

        remove: list[SkillDecision],

        add: list[SkillDecision],

        capacity: int,

    ):

        """
        Returns recruiter-approved replacement plan.

        Capacity means maximum number of skills
        the resume should contain after optimization.
        """

        # ---------------------------------------
        # Sort
        # ---------------------------------------

        keep.sort(
            key=lambda x: x.priority,
            reverse=True,
        )

        add.sort(
            key=lambda x: x.priority,
            reverse=True,
        )

        remove.sort(
            key=lambda x: x.priority,
        )

        # ---------------------------------------
        # Current Skill Count
        # ---------------------------------------

        current_count = len(keep)

        available_slots = max(
            0,
            capacity - current_count,
        )

        accepted_additions = []

        rejected_additions = []

        # ---------------------------------------
        # Fill Empty Capacity
        # ---------------------------------------

        for decision in add:

            if available_slots > 0:

                accepted_additions.append(
                    decision
                )

                available_slots -= 1

            else:

                rejected_additions.append(
                    decision
                )

        replacements = []

        # ---------------------------------------
        # Replace Low Priority Skills
        # ---------------------------------------

        removable = sorted(

            remove,

            key=lambda x: x.priority,

        )

        while (

            removable

            and

            rejected_additions

        ):

            remove_skill = removable.pop(0)

            add_skill = rejected_additions.pop(0)

            replacements.append(

                {

                    "remove": remove_skill,

                    "add": add_skill,

                }

            )

        return {

            "keep": keep,

            "add": accepted_additions,

            "replace": replacements,

        }