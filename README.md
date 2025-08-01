# CSFD Movie Downloader

A simple Django app to download top 300 movies from CSFD.cz under 30 seconds.

## Installation

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py collectstatic --noinput
```

## Usage

### Download data

```bash
uv run python manage.py download_data
# Starting data import from CSFD leaderboard...
# Data import completed in 24.68 seconds.
```

### Run the server

```bash
uv run python manage.py runserver
```

## Development

### Run tests

```bash
uv run pytest .
```

### Linting

```bash
# Install pre-commit hooks
uv run pre-commit install
```

# Final thoughts

## Search performance

While SQLite works well for this demo, potential improvements include:


* **SQLite FTS5**: Would enhance search speed and capabilities with better text queries and results ranking.


* **PostgreSQL**: Ideal for production, offering superior indexing, advanced search operators, and better concurrency.
