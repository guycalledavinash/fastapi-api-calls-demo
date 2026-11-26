"""FastAPI route-level tests using mocked upstream HTTP calls."""

import unittest
from unittest.mock import AsyncMock, patch

import httpx
from fastapi.testclient import TestClient

from app.main import app


class ApplicationRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_health_endpoint(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"message": "FastAPI API call demo is working!"},
        )

    def test_github_profile_route_returns_selected_fields(self):
        async def fake_getter(url: str) -> httpx.Response:
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

        with patch("app.routes.users.get_json_with_client", new=fake_getter):
            response = self.client.get("/users/github/octocat")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["login"], "octocat")
        self.assertEqual(response.json()["public_repos"], 8)
        self.assertEqual(response.json()["followers"], 999)

    def test_invalid_github_username_is_rejected_before_upstream_call(self):
        with patch(
            "app.routes.users.get_json_with_client",
            new_callable=AsyncMock,
        ) as getter:
            response = self.client.get("/users/github/not_a_valid_login")

        self.assertEqual(response.status_code, 422)
        getter.assert_not_awaited()

    def test_post_summary_route_combines_mocked_upstream_responses(self):
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

        async def fake_getter(url: str) -> httpx.Response:
            return httpx.Response(200, json=responses[url])

        with patch("app.routes.external_api.get_json_with_client", new=fake_getter):
            response = self.client.get("/external/posts/summary")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [(item["user_name"], item["post_count"]) for item in response.json()],
            [("bob", 2), ("alice", 1)],
        )


if __name__ == "__main__":
    unittest.main()
