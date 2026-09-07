# Togetherly

An early-stage Django application for managing shared household chores. Users
can belong to multiple households, with household membership and role support
for Owners, Admins, and Members.

## Requirements

- Python 3.14 or later
- Django 6.1.1

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you use `uv`, the equivalent commands are:

```bash
uv sync
uv run python manage.py migrate
```

Apply migrations when setting up the project:

```bash
python manage.py migrate
```

Create an administrator account if you need to use Django Admin:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

The application runs at <http://127.0.0.1:8000/>.

## Available endpoints

| Method | URL | Description | Authentication |
| --- | --- | --- | --- |
| `GET` | `/chores/` | Health check | Not required |
| `GET` | `/chores/households/` | List the signed-in user's households | Required |
| `POST` | `/chores/households/` | Create a household and become its Owner | Required |
| `GET` | `/admin/` | Django administration | Staff user required |

Create a household with form data:

```bash
curl -X POST http://127.0.0.1:8000/chores/households/ \
	-d "name=My Household"
```

Authenticated requests use Django's session authentication. Anonymous requests
to the household endpoint are redirected to Django's default login URL.

## Testing

Run the application tests with:

```bash
python manage.py test chores
```

Run Django's configuration checks with:

```bash
python manage.py check
```

## Project structure

```text
chores/              Django application
chores_management/   Django project configuration
_docs/               Product and implementation notes
backlog.md           Ordered MVP implementation tasks
manage.py             Django command-line entry point
```

## Project status

The project currently includes the initial household and membership foundation.
Invitation flows, chores, categories, authorization helpers, and the remaining
MVP workflow are tracked in `backlog.md`.
README.md