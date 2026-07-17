from pydantic import BaseModel, ConfigDict, EmailStr, Field

DEFAULT_PLAN = "Free plan"


class RegisterRequest(BaseModel):
    """Request model for user registration."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(
        ...,
        min_length=2,
        max_length=80,
        description="User's full name",
        examples=["John Doe"],
    )

    email: EmailStr = Field(
        ...,
        description="User email address",
        examples=["john@example.com"],
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password",
        examples=["StrongPassword123"],
    )


class LoginRequest(BaseModel):
    """Request model for user login."""

    model_config = ConfigDict(extra="forbid")

    email: EmailStr = Field(
        ...,
        description="Registered email address",
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password",
    )


class TokenResponse(BaseModel):
    """JWT authentication response."""

    access_token: str = Field(
        ...,
        description="JWT access token",
    )

    token_type: str = Field(
        default="bearer",
        description="Authentication scheme",
    )


class UserResponse(BaseModel):
    """Authenticated user information."""

    id: str = Field(
        ...,
        description="Unique user ID",
    )

    name: str = Field(
        ...,
        description="User's full name",
    )

    email: EmailStr = Field(
        ...,
        description="User email",
    )

    plan: str = Field(
        default=DEFAULT_PLAN,
        description="Current subscription plan",
    )