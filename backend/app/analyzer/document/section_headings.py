"""
app.analyzer.document.section_headings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Centralized resume section heading dictionary.

All known resume heading variations are defined here.
"""

from __future__ import annotations

SECTION_HEADINGS: dict[str, set[str]] = {
    "summary": {
        "summary",
        "professional summary",
        "profile",
        "career objective",
        "objective",
        "about",
        "about me",
    },

    "experience": {
    "experience",
    "work experience",
    "internship experience",
    "internships",
    "internship",
    "employment",
    "employment history",
    "work history",
    "career history",
    },

    "projects": {
        "projects",
        "project",
        "academic projects",
        "personal projects",
    },

    "skills": {
        "skills",
        "technical skills",
        "core skills",
        "technical expertise",
        "competencies",
    },

    "education": {
        "education",
        "academic background",
        "qualifications",
    },

    "certifications": {
        "certifications",
        "certification",
        "licenses",
    },

    "achievements": {
        "achievements",
        "accomplishments",
        "awards",
        "honors",
    },

    "publications": {
        "publications",
        "research",
    },

    "languages": {
        "languages",
    },

    "interests": {
        "interests",
        "hobbies",
    },

    "contact": {
        "contact",
        "contact information",
    },
}