from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureFlags:
    """
    Global feature switches.

    These control product capabilities
    without changing business logic.
    """

    # Authentication
    google_login: bool = True
    email_login: bool = True

    # Resume
    resume_history: bool = False
    pdf_download: bool = False
    resume_preview: bool = True
    resume_editor: bool = True

    # AI
    cover_letter: bool = False
    linkedin_optimizer: bool = False
    interview_preparation: bool = False

    # Platform
    referrals: bool = False
    coupons: bool = False
    analytics: bool = True


FEATURE_FLAGS = FeatureFlags()  