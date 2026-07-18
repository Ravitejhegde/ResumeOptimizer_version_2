# ADR-001: Preserve Original Formatting

## Status

Accepted

## Decision

ResumeOptimizer will only support Microsoft Word (.docx) files.

The application will never rebuild a resume from scratch.

Instead, it will:

1. Open the original document.
2. Modify only the textual content.
3. Preserve formatting, styles, layout, tables, spacing, and design.
4. Save the optimized resume as a new .docx file.

## Rationale

The user's existing resume design is valuable.

Our responsibility is to improve the content without changing the visual appearance.

This decision aligns with our product promise:

> Same Resume. Smarter Words.