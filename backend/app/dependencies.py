import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app import database
from app.utils.security import decode_access_token


logger = logging.getLogger(__name__)

security = HTTPBearer()


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Authenticate user using JWT access token.

    Returns:
        User document from MongoDB.

    Raises:
        HTTPException: If authentication fails.
    """

    token = creds.credentials

    try:
        payload = decode_access_token(token)

        # Check token purpose
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or invalid",
        )

    if database.db is None:
        logger.error(
            "Database connection is not initialized"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database unavailable",
        )


    user = await database.db.users.find_one(
        {
            "_id": user_id
        }
    )


    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )


    return user