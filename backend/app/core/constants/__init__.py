"""
Application-wide constants.

This package contains constants that are shared across the backend.
Avoid placing configurable values here—those belong in app.core.config.
"""

# =========================
# Application
# =========================

APP_NAME = "ResumeOptimizer"
APP_SLUG = "resume-optimizer"

# =========================
# Resume
# =========================

SUPPORTED_RESUME_EXTENSIONS = {
    ".docx",
}

# =========================
# Job Description
# =========================

SUPPORTED_JOB_DESCRIPTION_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx",
}

# =========================
# File Sizes
# =========================

MB = 1024 * 1024

MAX_RESUME_SIZE = 10 * MB
MAX_JOB_DESCRIPTION_SIZE = 10 * MB

# =========================
# AI
# =========================

DEFAULT_AI_TEMPERATURE = 0.2

# =========================
# Optimization
# =========================

DEFAULT_MAX_RETRIES = 3

DEFAULT_TIMEOUT_SECONDS = 120