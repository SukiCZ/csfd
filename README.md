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
# Data import completed in 29.61 seconds.
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
