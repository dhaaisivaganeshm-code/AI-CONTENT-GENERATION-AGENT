from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from app import database
from app.dependencies import get_current_user
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.utils.security import (
    create_access_token,
    hash_password,
    verify_password,
)

router = APIRouter(
    tags=["Authentication"],
)

DEFAULT_PLAN = "Free plan"


def check_database() -> None:
    """Ensure the database connection is available."""
    if database.db is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection unavailable.",
        )


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
) -> TokenResponse:
    """Register a new user."""

    check_database()

    email = request.email.lower().strip()

    existing_user = await database.db.users.find_one(
        {"email": email}
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    user_id = f"user_{uuid4().hex[:12]}"

    await database.db.users.insert_one(
        {
            "_id": user_id,
            "name": request.name.strip(),
            "email": email,
            "password_hash": hash_password(request.password),
            "plan": DEFAULT_PLAN,
        }
    )

    return TokenResponse(
        access_token=create_access_token(user_id)
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    request: LoginRequest,
) -> TokenResponse:
    """Authenticate a user and return a JWT access token."""

    check_database()

    email = request.email.lower().strip()

    user = await database.db.users.find_one(
        {"email": email}
    )

    if (
        user is None
        or not verify_password(
            request.password,
            user["password_hash"],
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    return TokenResponse(
        access_token=create_access_token(
            user["_id"]
        )
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
async def me(
    current_user: dict = Depends(get_current_user),
) -> UserResponse:
    """Return the authenticated user's profile."""

    return UserResponse(
        id=current_user["_id"],
        name=current_user["name"],
        email=current_user["email"],
        plan=current_user.get("plan", DEFAULT_PLAN),
    )