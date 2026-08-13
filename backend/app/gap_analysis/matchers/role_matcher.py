"""
app.gap_analysis.matchers.role_matcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Matches resume roles against job roles.
"""

from __future__ import annotations


class RoleMatcher:
    """
    Compares resume roles with target role.
    """

    def match(
        self,
        resume_roles: set[str],
        target_role: str,
    ) -> bool:

        return target_role in resume_roles