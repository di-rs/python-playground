FROM python:3.15-rc-alpine

COPY --from=ghcr.io/astral-sh/uv:0.13.0 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml ./

RUN uv lock
RUN uv sync --locked --no-dev --no-install-project

COPY . .

RUN uv sync --locked --no-dev

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]
