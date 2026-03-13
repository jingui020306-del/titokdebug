from dataclasses import dataclass

from fastapi import Depends, Header, Request


@dataclass
class CurrentUser:
    id: str
    name: str
    email: str


def current_user(request: Request, x_user_id: str | None = Header(default=None)) -> CurrentUser:
    """Dev session abstraction.

    TODO: Replace with real auth provider (Clerk/Auth.js/custom JWT) and permission checks.
    """
    user_id = x_user_id or getattr(request.state, "user_id", None) or "dev-user"
    return CurrentUser(
        id=user_id,
        name=f"开发用户 {user_id}",
        email=f"{user_id}@dev.local",
    )


def auth_guard(user: CurrentUser = Depends(current_user)) -> str:
    """Backward-compatible user id dependency for existing handlers."""
    return user.id
