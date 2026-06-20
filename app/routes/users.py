"""User-related routes."""

from fastapi import APIRouter, Path

from app.schemas import GithubUser
from app.services import fetch_github_user, get_json_with_client

router = APIRouter()


@router.get("/github/{username}", response_model=GithubUser)
async def github_user(
    username: str = Path(min_length=1, max_length=39, pattern=r"^[A-Za-z0-9-]+$"),
) -> GithubUser:
    """Return selected public profile information for a GitHub user."""
    return await fetch_github_user(username, get_json_with_client)
