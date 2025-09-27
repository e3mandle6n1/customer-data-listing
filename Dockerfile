# --- Stage 1: "Tester" ---
# This stage installs all dependencies and runs the tests.
FROM python:3.11-slim AS builder

WORKDIR /app

# Install production and testing dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

COPY app ./app
COPY tests ./tests
COPY data ./data

# Run the tests!
RUN pytest


# --- Stage 2: "Final Production Image" ---
# This stage starts fresh and only includes what's needed for production.
FROM python:3.11-slim

WORKDIR /app

# Install production dependencies only
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /app/app ./app
COPY --from=builder /app/data ./data

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]