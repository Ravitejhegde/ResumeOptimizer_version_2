"""
app.optimizer.prompts.job_prompt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds the job context prompt.
"""

from __future__ import annotations

from app.job_understanding.models.job_understanding import (
    JobUnderstanding,
)


def build_job_prompt(
    job: JobUnderstanding,
) -> str:
    """
    Build job context for AI.
    """

    return f"""
JOB UNDERSTANDING

Target Role:
{job.target_role}

Required Skills:
{", ".join(job.required_skills)}

Required Technologies:
{", ".join(job.required_technologies)}

Required Keywords:
{", ".join(job.required_keywords)}

Preferred Skills:
{", ".join(job.preferred_skills)}

Required Seniority:
{job.seniority}

Job Summary:
{job.summary}

Optimize the resume to align naturally
with these requirements.

Do not invent qualifications.
""".strip()