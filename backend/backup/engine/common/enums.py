from __future__ import annotations

from enum import Enum


class ObjectType(str, Enum):
    """
    Document object types.
    """

    TEXT = "text"
    HYPERLINK = "hyperlink"
    TABLE = "table"
    IMAGE = "image"
    HEADER = "header"
    FOOTER = "footer"


class SectionType(str, Enum):
    """
    Resume section types.
    """

    UNKNOWN = "unknown"

    SUMMARY = "summary"

    EXPERIENCE = "experience"

    PROJECTS = "projects"

    SKILLS = "skills"

    EDUCATION = "education"

    CERTIFICATIONS = "certifications"

    ACHIEVEMENTS = "achievements"

    PUBLICATIONS = "publications"

    LANGUAGES = "languages"

    INTERESTS = "interests"

    CUSTOM = "custom"


class ProtectionLevel(str, Enum):
    """
    Determines whether content can be modified.
    """

    LOCKED = "locked"

    RESTRICTED = "restricted"

    EDITABLE = "editable"


class OptimizationAction(str, Enum):
    """
    Actions the planner may request.
    """

    KEEP = "keep"

    REWRITE = "rewrite"

    EXPAND = "expand"

    REPLACE = "replace"

    REMOVE = "remove"

    REORDER = "reorder"

    RENAME = "rename"


class ValidationStatus(str, Enum):
    """
    Validation result.
    """

    PASSED = "passed"

    WARNING = "warning"

    FAILED = "failed"


class ConfidenceLevel(str, Enum):
    """
    AI confidence.
    """

    HIGH = "high"

    MEDIUM = "medium"

    LOW = "low"




