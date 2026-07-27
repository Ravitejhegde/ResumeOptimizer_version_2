from app.audit.audit_result import (
    AuditResult,
)

from app.audit.role_audit import (
    RoleAudit,
)

from app.audit.skill_audit import (
    SkillAudit,
)

from app.audit.plan_audit import (
    PlanAudit,
)

from app.audit.report_builder import (
    ReportBuilder,
)


class AuditEngine:
    """
    Executes the complete Brain Audit.
    """

    @classmethod
    def run(
        cls,
        resume,
        jd,
        reasoning,
        plan,
    ) -> AuditResult:

        result = AuditResult()

        # -----------------------------------------
        # Role Audit
        # -----------------------------------------

        RoleAudit.evaluate(

            resume,

            jd,

            result,

        )

        # -----------------------------------------
        # Skill Audit
        # -----------------------------------------

        SkillAudit.evaluate(

            reasoning,

            result,

        )

        # -----------------------------------------
        # Plan Audit
        # -----------------------------------------

        PlanAudit.evaluate(

            plan,

            result,

        )

        # -----------------------------------------
        # Print Report
        # -----------------------------------------

        ReportBuilder.print(
            result
        )

        return result




