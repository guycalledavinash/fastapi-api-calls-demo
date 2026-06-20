"""Response models used by the API routers."""

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class GithubUser(BaseModel):
    """Selected public GitHub profile fields returned by the demo API."""

    login: str
    name: str | None = None
    public_repos: int = Field(ge=0)
    followers: int = Field(ge=0)
    profile_url: HttpUrl


class UserPostSummary(BaseModel):
    """A JSONPlaceholder user enriched with their post count."""

    user_id: int
    user_name: str
    email: str
    post_count: int = Field(ge=0)


class Photo(BaseModel):
    """Selected JSONPlaceholder photo fields."""

    album_id: int = Field(alias="albumId")
    id: int
    title: str
    url: HttpUrl
    thumbnail_url: HttpUrl = Field(alias="thumbnailUrl")

    model_config = ConfigDict(populate_by_name=True)


class AlbumSummary(BaseModel):
    """A JSONPlaceholder album enriched with photo metadata."""

    album_id: int
    album_title: str
    photo_count: int = Field(ge=0)
    cover_photo: Photo | None = None


class HealthCheck(BaseModel):
    """Simple health-check response."""

    message: str
