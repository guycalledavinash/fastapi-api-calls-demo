"""Small async clients and data-shaping helpers for third-party APIs."""

from collections import Counter
from collections.abc import Awaitable, Callable
from typing import Any

import httpx
from fastapi import HTTPException, status

from app.schemas import AlbumSummary, GithubUser, Photo, UserPostSummary

DEFAULT_TIMEOUT_SECONDS = 10.0
RequestGetter = Callable[[str], Awaitable[httpx.Response]]


async def _get_json(url: str, getter: RequestGetter) -> Any:
    """Fetch JSON from a URL and translate upstream failures for API callers."""
    try:
        response = await getter(url)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Requested upstream resource was not found.",
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Upstream service returned an error.",
        ) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not reach upstream service.",
        ) from exc

    return response.json()


async def fetch_github_user(username: str, getter: RequestGetter) -> GithubUser:
    """Fetch a public GitHub profile and return a stable response shape."""
    data = await _get_json(f"https://api.github.com/users/{username}", getter)
    return GithubUser(
        login=data["login"],
        name=data.get("name"),
        public_repos=data["public_repos"],
        followers=data["followers"],
        profile_url=data["html_url"],
    )


async def fetch_post_summaries(getter: RequestGetter) -> list[UserPostSummary]:
    """Return JSONPlaceholder users ordered by descending post count."""
    posts = await _get_json("https://jsonplaceholder.typicode.com/posts", getter)
    users = await _get_json("https://jsonplaceholder.typicode.com/users", getter)

    post_counts = Counter(post["userId"] for post in posts)
    summaries = [
        UserPostSummary(
            user_id=user["id"],
            user_name=user["username"],
            email=user["email"],
            post_count=post_counts[user["id"]],
        )
        for user in users
    ]
    return sorted(summaries, key=lambda item: item.post_count, reverse=True)


async def fetch_album_summaries(getter: RequestGetter) -> list[AlbumSummary]:
    """Return JSONPlaceholder albums with photo counts and cover photos."""
    albums = await _get_json("https://jsonplaceholder.typicode.com/albums", getter)
    photos = await _get_json("https://jsonplaceholder.typicode.com/photos", getter)

    photo_counts = Counter(photo["albumId"] for photo in photos)
    cover_photos: dict[int, Photo] = {}
    for photo in sorted(photos, key=lambda item: item["id"]):
        cover_photos.setdefault(photo["albumId"], Photo.model_validate(photo))

    return [
        AlbumSummary(
            album_id=album["id"],
            album_title=album["title"],
            photo_count=photo_counts[album["id"]],
            cover_photo=cover_photos.get(album["id"]),
        )
        for album in albums
    ]


async def get_json_with_client(url: str) -> httpx.Response:
    """Default HTTP getter used by the route layer."""
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT_SECONDS) as client:
        return await client.get(url)
