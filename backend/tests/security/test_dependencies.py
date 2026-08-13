from __future__ import annotations

import uuid

import jwt
import pytest

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.core.config import settings
from app.core.security.dependencies import (
    get_current_active_user,
    get_current_user,
)
from app.core.security.jwt import jwt_service
from app.database.models.user import User
from app.database.repositories.user_repository import (
    UserRepository,
)


def create_test_user(
    db,
    *,
    active: bool = True,
    verified: bool = True,
) -> User:
    """
    Create a minimal authenticated test user.
    """

    user = User(
        id=str(uuid.uuid4()),
        email=f"security_{uuid.uuid4().hex[:8]}@example.com",
        password_hash="test-password-hash",
        name="Security Test",
        provider="email",
        country="IN",
        language="en",
        active=active,
        verified=verified,
    )

    UserRepository(db).create(user)

    return user


def credentials(
    token: str,
) -> HTTPAuthorizationCredentials:
    """
    Build HTTP Bearer credentials for dependency testing.
    """

    return HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token,
    )


def test_valid_access_token_returns_user(db):
    """
    A valid access token for an existing user
    must return the database User.
    """

    user = create_test_user(db)

    token = jwt_service.create_access_token(
        subject=user.id
    )

    result = get_current_user(
        credentials(token),
        db,
    )

    assert result.id == user.id
    assert result.email == user.email


def test_refresh_token_cannot_be_used_as_access_token(db):
    """
    A refresh token must never authenticate an API request.
    """

    user = create_test_user(db)

    token = jwt_service.create_refresh_token(
        subject=user.id
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials(token),
            db,
        )

    assert exc_info.value.status_code == 401
    assert (
        exc_info.value.detail
        == "Invalid or expired authentication token."
    )


def test_invalid_token_is_rejected(db):
    """
    A malformed token must result in HTTP 401.
    """

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials("this-is-not-a-valid-jwt"),
            db,
        )

    assert exc_info.value.status_code == 401
    assert (
        exc_info.value.detail
        == "Invalid or expired authentication token."
    )


def test_token_with_invalid_signature_is_rejected(db):
    """
    A correctly structured token signed with the
    wrong secret must be rejected.
    """

    user = create_test_user(db)

    payload = {
        "sub": user.id,
        "type": "access",
    }

    token = jwt.encode(
        payload,
        "wrong-secret",
        algorithm="HS256",
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials(token),
            db,
        )

    assert exc_info.value.status_code == 401


def test_token_without_user_id_is_rejected(db):
    """
    An access token without a subject/user ID
    must not authenticate anyone.
    """

    token = jwt.encode(
        {
            "type": "access",
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials(token),
            db,
        )

    assert exc_info.value.status_code == 401
    assert (
        exc_info.value.detail
        == "Invalid authentication token."
    )


def test_valid_token_for_nonexistent_user_is_rejected(db):
    """
    A validly signed access token is not sufficient.
    The user must actually exist in the database.
    """

    nonexistent_user_id = str(
        uuid.uuid4()
    )

    token = jwt_service.create_access_token(
        subject=nonexistent_user_id
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials(token),
            db,
        )

    assert exc_info.value.status_code == 401
    assert (
        exc_info.value.detail
        == "User not found."
    )


def test_inactive_user_is_rejected(db):
    """
    An authenticated but inactive user must receive 403.
    """

    user = create_test_user(
        db,
        active=False,
    )

    token = jwt_service.create_access_token(
        subject=user.id
    )

    authenticated_user = get_current_user(
        credentials(token),
        db,
    )

    assert authenticated_user.id == user.id
    assert authenticated_user.active is False

    with pytest.raises(HTTPException) as exc_info:
        get_current_active_user(
            authenticated_user,
        )

    assert exc_info.value.status_code == 403
    assert (
        exc_info.value.detail
        == "Account inactive."
    )


def test_active_user_is_accepted(db):
    """
    An authenticated active user must pass
    the active-user dependency.
    """

    user = create_test_user(
        db,
        active=True,
    )

    token = jwt_service.create_access_token(
        subject=user.id
    )

    authenticated_user = get_current_user(
        credentials(token),
        db,
    )

    result = get_current_active_user(
        authenticated_user,
    )

    assert result.id == user.id
    assert result.active is True