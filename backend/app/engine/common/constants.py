"""
ResumeOptimizer V3
Engine Constants

Only immutable engine-level constants belong here.
"""

# --------------------------------------------------
# Document
# --------------------------------------------------

MAX_DOCUMENT_PAGES = 10
MAX_TABLE_NESTING = 5

# --------------------------------------------------
# Layout Validation
# --------------------------------------------------

MIN_LAYOUT_SIMILARITY = 99.0

MAX_PARAGRAPH_EXPANSION = 0

MAX_PAGE_EXPANSION = 0

# --------------------------------------------------
# Text
# --------------------------------------------------

DEFAULT_PARAGRAPH_STYLE = "Normal"

# --------------------------------------------------
# Object Types
# --------------------------------------------------

OBJECT_TEXT = "text"

OBJECT_HYPERLINK = "hyperlink"

OBJECT_TABLE = "table"

OBJECT_IMAGE = "image"

# --------------------------------------------------
# Protection Reasons
# --------------------------------------------------

LOCK_PERSONAL_INFORMATION = "personal_information"

LOCK_COMPANY_NAME = "company_name"

LOCK_EDUCATION = "education"

LOCK_DATE = "date"

LOCK_PROJECT_TITLE = "project_title"

# --------------------------------------------------
# Resume Sections
# --------------------------------------------------

SECTION_SUMMARY = "summary"

SECTION_EXPERIENCE = "experience"

SECTION_PROJECTS = "projects"

SECTION_SKILLS = "skills"

SECTION_EDUCATION = "education"

SECTION_CERTIFICATIONS = "certifications"