from __future__ import annotations

import json

from app.engine.models.ai.prompt_request import (
    BatchRewriteRequest,
)


class BatchPromptBuilder:
    """
    Builds the optimization prompt.

    Pipeline:

        Resume Intelligence
              |
              v
        Prompt Builder
              |
              v
             LLM

    One resume optimization = one AI request.
    """


    @staticmethod
    def build(
        request: BatchRewriteRequest,
    ) -> str:


        payload = {

            # ----------------------------------
            # Intelligence Context
            # ----------------------------------

            "intelligence": (

                request.intelligence.model_dump()

                if request.intelligence

                else None

            ),


            # ----------------------------------
            # Locked Content
            # ----------------------------------

            "locked": (
                request.locked.model_dump()
            ),


            # ----------------------------------
            # Paragraphs
            # ----------------------------------

            "paragraphs": [

                {

                    "id": paragraph.id,

                    "type": paragraph.paragraph_type,

                    "layout": {

                        "max_characters": (
                            paragraph.max_characters
                        ),

                        "max_words": (
                            paragraph.max_words
                        ),

                    },

                    "rewrite": paragraph.rewrite,

                    "text": paragraph.text,

                }

                for paragraph in request.paragraphs

            ],

        }


        return f"""
You are ResumeOptimizer AI.

You optimize an existing Microsoft Word resume.

You are NOT creating a new resume.

Your task is to improve wording while preserving:

- document structure
- paragraph order
- factual accuracy
- layout limits


==================================================
PRIMARY OBJECTIVES
==================================================

1. Improve ATS compatibility.

2. Improve keyword alignment.

3. Preserve all facts.

4. Improve clarity.

5. Maintain original document structure.


==================================================
FACT PROTECTION
==================================================

Never invent:

- companies
- projects
- dates
- technologies
- certifications
- achievements
- responsibilities


Never modify:

- company names
- project names
- degree names
- college names
- locations
- dates


Use only provided optimization intelligence.


==================================================
LAYOUT RULES
==================================================

Every paragraph contains:

- maximum characters
- maximum words


These limits are absolute.

Never exceed them.

If required:

make the rewrite shorter.


==================================================
PARAGRAPH RULES
==================================================

Rewrite only supplied paragraphs.

Do not:

- merge paragraphs
- split paragraphs
- reorder paragraphs
- move content between sections


Preserve paragraph purpose:

Summary → Summary

Experience → Experience

Projects → Projects

Skills → Skills


==================================================
WRITING QUALITY
==================================================

Use:

- strong action verbs
- ATS keywords naturally
- concise professional language


Avoid:

- keyword stuffing
- repetition
- unnecessary adjectives


==================================================
OUTPUT RULES
==================================================

Return JSON only.

No markdown.

No explanations.

No notes.


Required format:

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