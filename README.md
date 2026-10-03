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

## Run with Docker

Build the image from the repository root:

```bash
docker build -t fastapi-api-calls-demo .
```

Start the container and publish the application's port:

```bash
docker run --rm -p 8000:8000 fastapi-api-calls-demo
```

The application listens on port `8000`; open <http://127.0.0.1:8000/docs> after it starts. The Docker image uses a multi-stage build to create dependency wheels outside the runtime image, then runs the slim final image as a non-root user. It copies only the application package and its installed dependencies into the final image, and does not include API credentials or secrets.

## Development checks

```bash
python -m compileall app
python -m unittest discover -s tests
```
