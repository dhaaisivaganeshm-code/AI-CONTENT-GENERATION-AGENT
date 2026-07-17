import hashlib
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.config import settings


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using SHA-256.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain-text password against its hash.
    """
    return hash_password(plain_password) == hashed_password


def create_access_token(subject: str) -> str:
    """
    Create a signed JWT access token.
    """

    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "iat": issued_at,
        "exp": expires_at,
        "type": "access",
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.

    Raises:
        JWTError: If the token is invalid or expired.
    """

    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )