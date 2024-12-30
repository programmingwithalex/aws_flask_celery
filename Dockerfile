# https://hub.docker.com/_/python
FROM python:3.13-slim

RUN useradd -m myuser

WORKDIR /app

# Avoid cache purge by adding requirements first
COPY pyproject.toml .

RUN pip install pip --upgrade
RUN pip install wheel uv

# `uv` is faster alternative to `pip` and `requirements.txt`
RUN uv pip install -r pyproject.toml --system --no-cache-dir

# Add the rest of the files
COPY . .

# Set ownership and permissions for the non-root user
RUN chown -R myuser:myuser /app
RUN chmod -R 755 /app

# need to leave WORKDIR as /app instead of /app/proj to preserve relative imports

# Specify the command to run the application - not needed if using docker-compose
# CMD ["gunicorn", "app:app", "-w", "4", "-b", "0.0.0.0:8000"]
