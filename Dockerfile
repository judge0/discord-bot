FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_NO_CACHE=1 \
    UV_PYTHON_DOWNLOADS=never \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY bot ./bot
RUN uv sync --locked --no-dev --no-editable \
    && useradd --create-home --uid 10001 judge0

USER judge0

CMD ["judge0-discord-bot"]

LABEL maintainer="Herman Zvonimir Dosilovic <hermanz.dosilovic@gmail.com>"
