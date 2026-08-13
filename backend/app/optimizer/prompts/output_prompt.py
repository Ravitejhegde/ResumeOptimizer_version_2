"""
app.optimizer.prompts.output_prompt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Defines the required AI response format.
"""

from __future__ import annotations


OUTPUT_PROMPT = """
OUTPUT FORMAT

Return ONLY valid JSON.

Do not return Markdown.

Do not wrap JSON inside code blocks.

The JSON must follow this schema:

{
    "paragraph_updates": [
        {
            "paragraph_id": "P00001",
            "optimized_text": "Improved paragraph.",
            "reason": "Added ATS keywords.",
            "confidence": 0.95
        }
    ]
}

Rules

1. Return only paragraphs requested.

2. Do not create new paragraph IDs.

3. Preserve paragraph IDs exactly.

4. If no improvement is possible,
return an empty list.

Example:

{
    "paragraph_updates": []
}
"""