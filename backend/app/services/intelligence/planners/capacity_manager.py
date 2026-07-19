from app.services.intelligence.models import (
    ResumeAnalysis,
    SkillDecision,
)


class CapacityManager:
    """
    Calculates how many skills can be added
    without breaking the original resume layout.
    """

    @staticmethod
    def calculate(

        resume: ResumeAnalysis,

        keep: list[SkillDecision],

        remove: list[SkillDecision],

        add: list[SkillDecision],

    ):

        # -------------------------------------
        # Original Resume Capacity
        # -------------------------------------

        capacity = resume.total_skill_capacity

        # -------------------------------------
        # Current Keep Count
        # -------------------------------------

        keep_count = len(keep)

        # -------------------------------------
        # Empty Slots
        # -------------------------------------

        empty_slots = max(

            0,

            capacity - keep_count,

        )

        # -------------------------------------
        # Add Without Replacement
        # -------------------------------------

        accepted = []

        waiting = []

        for decision in add:

            if empty_slots > 0:

                accepted.append(
                    decision
                )

                empty_slots -= 1

            else:

                waiting.append(
                    decision
                )

        # -------------------------------------
        # Replacement Candidates
        # -------------------------------------

        removable = sorted(

            remove,

            key=lambda x: x.priority,

        )

        replacements = []

        while removable and waiting:

            remove_skill = removable.pop(0)

            add_skill = waiting.pop(0)

            replacements.append(

                (

                    remove_skill,

                    add_skill,

                )

            )

        # -------------------------------------
        # Statistics
        # -------------------------------------

        return {

            "capacity": capacity,

            "keep": keep,

            "add": accepted,

            "replace": replacements,

            "rejected": waiting,

        }