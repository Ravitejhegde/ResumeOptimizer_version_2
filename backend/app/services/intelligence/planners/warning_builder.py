from app.services.intelligence.models import (
    OptimizationPlan,
)


class WarningBuilder:
    """
    Generates optimization warnings.
    These warnings are useful for:
    - UI
    - AI Prompt
    - Debugging
    """

    @classmethod
    def build(

        cls,

        resume,

        jd,

        plan: OptimizationPlan,

    ) -> list[str]:

        warnings = []

        # -----------------------------------
        # Role mismatch
        # -----------------------------------

        if resume.detected_role != jd.target_role:

            warnings.append(

                f"Role transition detected: "
                f"{resume.detected_role} → {jd.target_role}"

            )

        # -----------------------------------
        # Missing Skills
        # -----------------------------------

        if len(plan.add):

            warnings.append(

                f"{len(plan.add)} required technologies "
                f"are missing."

            )

        # -----------------------------------
        # Large Transition
        # -----------------------------------

        if len(plan.add) > 8:

            warnings.append(

                "Large career transition detected."

            )

        # -----------------------------------
        # Capacity Warning
        # -----------------------------------

        if resume.total_skill_capacity < len(plan.add):

            warnings.append(

                "Resume has limited skill capacity."

            )

        # -----------------------------------
        # Empty Summary
        # -----------------------------------

        if hasattr(resume, "summary"):

            if resume.summary.words < 10:

                warnings.append(

                    "Professional summary is too short."

                )

        return warnings