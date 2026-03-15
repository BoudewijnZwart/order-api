# ── Builder stage ────────────────────────────────────────────────────────────
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

# Enable bytecode compilation and use the system Python in the run stage
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install dependencies first (better layer caching)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the source and install the project itself
COPY . .
RUN uv sync --frozen --no-dev


# ── Run stage ─────────────────────────────────────────────────────────────────
FROM python:3.13-slim AS run

WORKDIR /app

# Create a non-root user for security
RUN addgroup --system app && adduser --system --ingroup app app

# Copy the virtual environment and application source from the builder
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app /app

USER app

# Prepend the venv binaries to PATH
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "order_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
