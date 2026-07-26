from __future__ import annotations

import json

from app.services.ai.batch.batch_models import (
    BatchRewriteRequest,
)


class BatchPromptBuilder:
    """
    Builds a single prompt for rewriting
    an entire resume.

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

        payload = {
            "target_role": request.target_role,
            "selected_skills": request.selected_skills,
            "locked": request.locked.model_dump(),
            "paragraphs": [
                {
                    "id": paragraph.id,
                    "type": paragraph.type,
                    "layout": {
                        "target_characters": paragraph.max_characters,
                        "hard_limit_characters": paragraph.max_characters,
                        "target_words": paragraph.max_words,
                        "hard_limit_words": paragraph.max_words,
                        "preserve_layout": True,
                    },
                    "rewrite": paragraph.rewrite,
                    "text": paragraph.text,
                }
                for paragraph in request.paragraphs
            ],
        }

        return f"""
You are ResumeOptimizer AI.

Your job is to optimize an existing DOCX resume for ATS while preserving its original layout.

The optimization will be inserted back into the original Microsoft Word document.

Breaking the layout is considered a failure.

==================================================
PRIORITY ORDER
==================================================

Priority 1
-----------
Preserve document layout.

Priority 2
-----------
Never exceed layout limits.

Priority 3
-----------
Never invent information.

Priority 4
-----------
Improve ATS score.

Priority 5
-----------
Improve grammar and readability.

==================================================
STRICT RULES
==================================================

1. Never invent experience.

2. Never invent projects.

3. Never invent technologies.

4. Never change:

   • Company names
   • Dates
   • Degree names
   • College names
   • Project names

5. Preserve the original meaning.

6. Improve ATS keywords naturally.

7. Remove weak wording.

8. Use strong action verbs.

9. Keep professional language.

10. Preserve paragraph type.

11. Do not change paragraph order.

12. Never merge paragraphs.

13. Never split paragraphs.

14. Never create extra paragraphs.

15. Never create bullet points unless they already exist.

16. Never create blank lines.

17. Never output Markdown.

18. Never output explanations.

19. Return ONLY valid JSON.

==================================================
LAYOUT RULES
==================================================

Every paragraph contains layout constraints.

For EACH paragraph:

• Stay close to target_words.

• Stay close to target_characters.

• NEVER exceed:

    hard_limit_words

or

    hard_limit_characters

If your rewrite exceeds a limit:

Rewrite it internally until it fits.

Do NOT return an oversized paragraph.

==================================================
QUALITY RULES
==================================================

Every rewritten paragraph must:

✓ Improve ATS

✓ Improve readability

✓ Preserve facts

✓ Preserve formatting intent

✓ Fit inside the supplied layout budget

==================================================
SELF VALIDATION
==================================================

Before returning JSON, verify:

✓ Valid JSON

✓ Every paragraph has an id

✓ Every paragraph has text

✓ No Markdown

✓ No explanations

✓ No missing paragraphs

✓ No extra paragraphs

✓ All layout limits satisfied

If any check fails,

rewrite internally before returning.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY this JSON:

{{
    "paragraphs": [
        {{
            "id": "P00001",
            "text": "Optimized paragraph"
        }}
    ]
}}

==================================================
RESUME DATA
==================================================

{json.dumps(payload, indent=2)}
""".strip()