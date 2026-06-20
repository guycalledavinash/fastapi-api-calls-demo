# FastAPI API Calls Demo

A small FastAPI app that demonstrates how to call third-party APIs asynchronously, validate the responses with Pydantic models, and expose a cleaner API to clients.

## Features

- `GET /` health check.
- `GET /users/github/{username}` fetches selected public GitHub profile fields.
- `GET /external/posts/summary` combines JSONPlaceholder users and posts into per-user post counts.
- `GET /external/albums/summary` combines JSONPlaceholder albums and photos into album summaries with cover photos.
- Upstream HTTP errors are converted into API-friendly `404` or `502` responses.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs> to explore the interactive API documentation.

## Development checks

```bash
python -m compileall app
python -m unittest discover -s tests
```
