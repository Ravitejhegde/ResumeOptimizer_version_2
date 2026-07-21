class RoleAudit:

    @classmethod
    def evaluate(
        cls,
        resume,
        jd,
        result,
    ):

        result.resume_role = (
            resume.detected_role
        )

        result.jd_role = (
            jd.target_role
        )

        if (
            resume.detected_role
            == "Unknown"
        ):

            result.add_warning(
                "Resume role could not be detected."
            )

        return result