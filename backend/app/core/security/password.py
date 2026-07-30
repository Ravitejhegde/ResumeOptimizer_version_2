"""
Password hashing and verification utilities.
"""

from __future__ import annotations

from passlib.context import CryptContext



# ==========================================================
# Password Hasher
# ==========================================================

class PasswordHasher:
    """
    Handles password hashing and verification.

    Responsibilities:
        - Hash plain passwords.
        - Verify passwords.

    Does not:
        - Manage users.
        - Access database.
        - Handle authentication flow.
    """


    def __init__(self) -> None:

        self._context = CryptContext(
            schemes=[
                "bcrypt"
            ],
            deprecated="auto",
        )



    # ======================================================
    # Hash Password
    # ======================================================

    def hash(
        self,
        password: str,
    ) -> str:
        """
        Convert plain password into secure bcrypt hash.
        """


        if not password:

            raise ValueError(
                "Password cannot be empty."
            )


        if len(password) < 8:

            raise ValueError(
                "Password must contain minimum 8 characters."
            )


        return self._context.hash(
            password
        )



    # ======================================================
    # Verify Password
    # ======================================================

    def verify(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """
        Verify plain password against bcrypt hash.
        """


        if not plain_password:

            return False


        if not hashed_password:

            return False


        try:

            return self._context.verify(
                plain_password,
                hashed_password,
            )

        except Exception:

            return False



# ==========================================================
# Singleton Instance
# ==========================================================

password_hasher = PasswordHasher()



# ==========================================================
# Backward Compatible Functions
# ==========================================================

def hash_password(
    password: str,
) -> str:
    """
    Hash password wrapper.
    """

    return password_hasher.hash(
        password
    )



def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify password wrapper.
    """

    return password_hasher.verify(
        plain_password,
        hashed_password,
    )