from __future__ import annotations

import json

from app.services.ai.batch.batch_models import (
    BatchRewriteRequest,
)


class BatchPromptBuilder:
    """
    Builds the single optimization prompt.

    One Resume
        ↓
    One Prompt
        ↓
    One AI Call
    """

    @staticmethod
    def build(
        request: BatchRewriteRequest,
    ) -> str:

        strategy = request.optimization_strategy

        payload = {

            # ------------------------------------------
            # Resume Intelligence
            # ------------------------------------------

            "target_role": request.target_role,

            "optimization_strategy": (

                {

                    "role": strategy.role,

                    "role_family": strategy.role_family,

                    "categories": strategy.categories,

                    "targets": [

                        {

                            "technology": target.technology,

                            "category": target.category,

                            "score": target.score,

                            "action": target.action,

                            "section": target.section,

                            "paragraph_id": target.paragraph_id,

                            "reason": target.reason,

                        }

                        for target in strategy.targets

                    ],

                    "summary_targets": strategy.summary_targets,

                    "experience_targets": strategy.experience_targets,

                    "project_targets": strategy.project_targets,

                    "skills_targets": strategy.skills_targets,

                    "ignored": strategy.ignored,

                }

                if strategy

                else None

            ),

            # Temporary compatibility

            "selected_skills": request.selected_skills,

            # Locked entities

            "locked": request.locked.model_dump(),

            # Paragraphs

            "paragraphs": [

                {

                    "id": paragraph.id,

                    "type": paragraph.type,

                    "layout": {

                        "max_characters": paragraph.max_characters,

                        "max_words": paragraph.max_words,

                    },

                    "rewrite": paragraph.rewrite,

                    "text": paragraph.text,

                }

                for paragraph in request.paragraphs

            ],

        }

        return f"""
You are ResumeOptimizer AI.

You optimize existing Microsoft Word resumes.

Your task is NOT to create a new resume.

Your task is to improve the existing resume while preserving its layout.

==================================================
PRIMARY OBJECTIVES
==================================================

1. Preserve document structure.

2. Improve ATS quality.

3. Preserve every factual statement.

4. Improve readability.

5. Never exceed layout limits.

==================================================
STRICT RULES
==================================================

Never invent:

• experience

• projects

• companies

• dates

• technologies

• certifications

• achievements

Never modify:

• company names

• project names

• college names

• degree names

• dates

Use ONLY technologies supplied inside the optimization strategy.

Promote technologies only where instructed.

Never duplicate technologies.

Never move technologies between unrelated sections.

Never change paragraph order.

Never merge paragraphs.

Never split paragraphs.

Never generate Markdown.

Never generate explanations.

Never generate notes.

Return JSON only.

==================================================
LAYOUT CONTRACT
==================================================

Every paragraph contains a maximum word count and maximum character count.

These limits are absolute.

The supplied limits already include a safety margin.

Never try to use the entire budget.

If a rewrite is close to the limit:

rewrite it shorter.

Repeat internally until BOTH limits are satisfied.

Do not return oversized paragraphs.

==================================================
PARAGRAPH RULES
==================================================

Each paragraph is independent.

Rewrite ONLY the supplied paragraph.

Preserve its purpose.

Summary remains summary.

Experience remains experience.

Projects remain projects.

Skills remain skills.

==================================================
QUALITY
==================================================

Use:

• strong action verbs

• ATS keywords naturally

• concise wording

• professional grammar

Avoid:

• keyword stuffing

• repetition

• unnecessary adjectives

==================================================
SELF VALIDATION
==================================================

Before producing JSON verify:

✓ valid JSON

✓ every paragraph exists

✓ every paragraph has an id

✓ every paragraph has text

✓ paragraph order unchanged

✓ no extra paragraphs

✓ no missing paragraphs

✓ character limit satisfied

✓ word limit satisfied

If any validation fails:

rewrite internally until valid.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY:

{{
    "paragraphs": [

        {{

            "id": "P00001",

            "text": "Optimized paragraph"

        }}

    ]
}}

==================================================
INPUT
==================================================

{json.dumps(payload, indent=2)}
""".strip()




