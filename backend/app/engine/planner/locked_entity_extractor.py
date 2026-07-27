from __future__ import annotations

import re

from app.engine.models.document import Document

from app.services.ai.batch.batch_models import (
    LockedEntities,
)


class LockedEntityExtractor:
    """
    Extracts immutable entities from a resume.

    These values must never be modified by AI.
    """

    COMPANY_SUFFIXES = (
        "Solutions",
        "Systems",
        "Ltd",
        "Limited",
        "Private Limited",
        "Pvt Ltd",
        "Inc",
        "LLP",
    )

    DEGREE_KEYWORDS = (
        "Bachelor",
        "Master",
        "BCA",
        "MCA",
        "B.Tech",
        "M.Tech",
        "B.E",
        "M.E",
        "PhD",
    )

    DATE_PATTERN = re.compile(
        r"\b\d{1,2}/\d{4}\b|\b\d{4}\b"
    )

    @classmethod
    def extract(
        cls,
        document: Document,
    ) -> LockedEntities:

        locked = LockedEntities()

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if not text:
                continue

            # Dates
            locked.dates.extend(
                cls.DATE_PATTERN.findall(text)
            )

            # Degrees
            if any(
                keyword.lower() in text.lower()
                for keyword in cls.DEGREE_KEYWORDS
            ):
                locked.degrees.append(text)

            # Companies
            if any(
                suffix.lower() in text.lower()
                for suffix in cls.COMPANY_SUFFIXES
            ):
                locked.companies.append(text)

            # Education
            if (
                paragraph.section
                and paragraph.section.lower()
                == "education"
            ):
                locked.colleges.append(text)

            # Projects
            if (
                paragraph.section
                and paragraph.section.lower()
                == "projects"
            ):
                locked.project_names.append(text)

        locked.companies = sorted(set(locked.companies))
        locked.dates = sorted(set(locked.dates))
        locked.degrees = sorted(set(locked.degrees))
        locked.colleges = sorted(set(locked.colleges))
        locked.project_names = sorted(set(locked.project_names))
        locked.locations = sorted(set(locked.locations))

        return locked




