"""
Security utilities for ResumeOptimizer.
"""

from .dependencies import (
    get_current_active_user,
    get_current_user,
    oauth2_scheme,
)
from .jwt import (
    ALGORITHM,
    create_access_token,
    decode_token,
)
from .password import (
    hash_password,
    verify_password,
)

__all__ = [
    # Password
    "hash_password",
    "verify_password",

    # JWT
    "ALGORITHM",
    "create_access_token",
    "decode_token",

    # Dependencies
    "oauth2_scheme",
    "get_current_user",
    "get_current_active_user",
]