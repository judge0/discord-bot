FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY bot ./bot
RUN pip install --no-cache-dir . \
    && useradd --create-home --uid 10001 judge0

USER judge0

CMD ["python", "-m", "bot"]

LABEL maintainer="Herman Zvonimir Dosilovic <hermanz.dosilovic@gmail.com>"
