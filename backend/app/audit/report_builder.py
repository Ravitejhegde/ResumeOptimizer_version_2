class ReportBuilder:

    @classmethod
    def print(
        cls,
        result,
    ):

        print()

        print("=" * 60)
        print("BRAIN AUDIT REPORT")
        print("=" * 60)

        print(
            f"Resume Role : {result.resume_role}"
        )

        print(
            f"JD Role     : {result.jd_role}"
        )

        print()

        print("Matched Skills")

        for item in result.matched_skills:

            print(
                f"  ✓ {item}"
            )

        print()

        print("Missing Skills")

        for item in result.missing_skills:

            print(
                f"  + {item}"
            )

        print()

        print("Extra Skills")

        for item in result.extra_skills:

            print(
                f"  - {item}"
            )

        print()

        print("Recommendations")

        for item in result.recommendations:

            print(
                f"  • {item}"
            )

        print()

        print("Risks")

        for item in result.risks:

            print(
                f"  ! {item}"
            )

        print()

        print("Warnings")

        for item in result.warnings:

            print(
                f"  ⚠ {item}"
            )

        print()

        print("Validation Errors")

        for item in result.validation_errors:

            print(
                f"  ✗ {item}"
            )

        print()

        print(
            "Status :",
            "PASS"
            if result.passed
            else "FAIL",
        )

        print("=" * 60)




