from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from app.database import db
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
    prefix="/auth",
    tags=["Authentication"],
)


def _check_database():
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection unavailable.",
        )


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(body: RegisterRequest):
    _check_database()

    email = body.email.lower().strip()

    existing = await db.users.find_one(
        {"email": email}
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    user_id = f"user_{uuid4().hex[:12]}"

    await db.users.insert_one(
        {
            "_id": user_id,
            "name": body.name.strip(),
            "email": email,
            "password_hash": hash_password(body.password),
            "plan": "Free plan",
        }
    )

    return TokenResponse(
        access_token=create_access_token(user_id)
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(body: LoginRequest):
    _check_database()

    email = body.email.lower().strip()

    user = await db.users.find_one(
        {"email": email}
    )

    if (
        not user
        or not verify_password(
            body.password,
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
    user=Depends(get_current_user),
):
    return UserResponse(
        id=user["_id"],
        name=user["name"],
        email=user["email"],
        plan=user.get("plan", "Free plan"),
    )