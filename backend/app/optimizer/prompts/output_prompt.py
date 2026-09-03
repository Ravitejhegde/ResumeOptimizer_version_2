"""
app.optimizer.prompts.output_prompt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Defines the required AI response format.
"""

from __future__ import annotations


OUTPUT_PROMPT = """
OUTPUT FORMAT

Return ONLY valid JSON.

Do NOT return Markdown.

Do NOT wrap JSON inside code blocks.

The JSON must follow this schema:

{
    "paragraph_updates": [
        {
            "paragraph_id": "p1",
            "section": "Professional Summary",
            "original_text": "Original paragraph text.",
            "optimized_text": "Improved paragraph text.",
            "confidence": 0.95,
            "reason": "Improved ATS keyword alignment."
        }
    ]
}

RULES

1. Return only paragraphs that require optimization.

2. Use paragraph IDs exactly as provided
in the ORIGINAL RESUME.

3. Never create new paragraph IDs.

4. Never remove paragraphs.

5. Preserve paragraph IDs exactly.

6. The original_text must match the supplied
paragraph text.

7. optimized_text must contain only the
rewritten paragraph text.

8. Do not return Markdown inside optimized_text.

9. Do not return explanations outside the JSON.

10. If no improvement is possible, return:

{
    "paragraph_updates": []
}

The response MUST be valid JSON.
"""