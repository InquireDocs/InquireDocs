FROM python:3.13-slim
LABEL maintainer="Julian Nonino <noninojulian@gmail.com>"

# Build Arguments
ARG USER_NAME=appuser
ARG USER_ID=1000
ARG GROUP_NAME=appuser
ARG GROUP_ID=1000
ARG APP_PORT=8000
ARG FAST_API_WORKERS=4

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=$APP_PORT
ENV WORKERS=$FAST_API_WORKERS

# Install build tools and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user and group
RUN addgroup --gid $GROUP_ID $GROUP_NAME && \
    adduser --uid $USER_ID --gid $GROUP_ID --disabled-password --gecos "" $USER_NAME

# Create application directory and set permissions
WORKDIR /code
RUN chown $USER_NAME:$GROUP_NAME /code

# Copy dependencies and install
COPY --chown=$USER_NAME:$GROUP_NAME requirements.txt /code/
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir --requirement requirements.txt

# Switch to non-root user
USER $USER_ID

# Copy the rest of the application code
COPY --chown=$USER_NAME:$GROUP_NAME ./app /code/app

# Expose the port
EXPOSE $APP_PORT

# Healthcheck
# HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
#     CMD curl --fail http://localhost:$APP_PORT/health || exit 1

# Start the application
# CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT", "--workers", "$WORKERS"]
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers $WORKERS"]
