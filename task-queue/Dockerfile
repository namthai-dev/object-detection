FROM python:3.9

WORKDIR /

# Download Poetry
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN mkdir /app/ /var/logs/

COPY ./pyproject.toml poetry.lock /

# Include poetry into the path
ENV PATH="${PATH}:/root/.local/bin"

# Prevent poetry creating virtual environment before installing depedencies
RUN poetry config virtualenvs.create false

# Expose port for the application
EXPOSE 8000

# Install dependencies
# Use a Docker BuildKit cache mountto speed up the installation of Python dependencies
RUN --mount=type=cache,target=/root/.cache/poetry poetry install

COPY ./src /src/
