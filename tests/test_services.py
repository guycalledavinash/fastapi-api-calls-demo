import unittest

import httpx
from fastapi import HTTPException

from app.services import fetch_album_summaries, fetch_github_user, fetch_post_summaries


class ServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_fetch_github_user_shapes_response(self):
        async def getter(url: str) -> httpx.Response:
            self.assertEqual(url, "https://api.github.com/users/octocat")
            return httpx.Response(
                200,
                json={
                    "login": "octocat",
                    "name": "The Octocat",
                    "public_repos": 8,
                    "followers": 999,
                    "html_url": "https://github.com/octocat",
                },
            )

        result = await fetch_github_user("octocat", getter)

        self.assertEqual(result.login, "octocat")
        self.assertEqual(result.public_repos, 8)
        self.assertEqual(str(result.profile_url), "https://github.com/octocat")

    async def test_fetch_post_summaries_sorts_by_post_count(self):
        responses = {
            "https://jsonplaceholder.typicode.com/posts": [
                {"userId": 2},
                {"userId": 1},
                {"userId": 2},
            ],
            "https://jsonplaceholder.typicode.com/users": [
                {"id": 1, "username": "alice", "email": "alice@example.com"},
                {"id": 2, "username": "bob", "email": "bob@example.com"},
            ],
        }

        async def getter(url: str) -> httpx.Response:
            return httpx.Response(200, json=responses[url])

        result = await fetch_post_summaries(getter)

        self.assertEqual([item.user_name for item in result], ["bob", "alice"])
        self.assertEqual([item.post_count for item in result], [2, 1])

    async def test_fetch_album_summaries_uses_lowest_photo_id_as_cover(self):
        responses = {
            "https://jsonplaceholder.typicode.com/albums": [
                {"id": 10, "title": "Summer"},
            ],
            "https://jsonplaceholder.typicode.com/photos": [
                {
                    "albumId": 10,
                    "id": 2,
                    "title": "second",
                    "url": "https://example.com/2.jpg",
                    "thumbnailUrl": "https://example.com/2-thumb.jpg",
                },
                {
                    "albumId": 10,
                    "id": 1,
                    "title": "first",
                    "url": "https://example.com/1.jpg",
                    "thumbnailUrl": "https://example.com/1-thumb.jpg",
                },
            ],
        }

        async def getter(url: str) -> httpx.Response:
            return httpx.Response(200, json=responses[url])

        result = await fetch_album_summaries(getter)

        self.assertEqual(result[0].photo_count, 2)
        self.assertEqual(result[0].cover_photo.id, 1)

    async def test_upstream_404_becomes_http_exception(self):
        async def getter(url: str) -> httpx.Response:
            request = httpx.Request("GET", url)
            return httpx.Response(404, request=request)

        with self.assertRaises(HTTPException) as context:
            await fetch_github_user("missing", getter)

        self.assertEqual(context.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()
