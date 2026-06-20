"""Routes that demonstrate consuming external JSON APIs."""

from fastapi import APIRouter

from app.schemas import AlbumSummary, UserPostSummary
from app.services import fetch_album_summaries, fetch_post_summaries, get_json_with_client

router = APIRouter()


@router.get("/posts/summary", response_model=list[UserPostSummary])
async def post_summaries() -> list[UserPostSummary]:
    """Return JSONPlaceholder users enriched with their number of posts."""
    return await fetch_post_summaries(get_json_with_client)


@router.get("/albums/summary", response_model=list[AlbumSummary])
async def album_summaries() -> list[AlbumSummary]:
    """Return JSONPlaceholder albums enriched with photo counts and cover photos."""
    return await fetch_album_summaries(get_json_with_client)
