# Travel Planner API

Django + DRF backend for managing travel projects and places with validation through the Art Institute of Chicago API.

## Features
- Travel project CRUD
- Add places to a project
- List/get places inside a project
- Update place notes and visited status
- Project auto-completion when all places are visited
- Deletion rule: project cannot be deleted if any place is visited
- Max 10 places per project
- No duplicate external place in the same project
- External place validation via Art Institute API
- Basic Auth protection for API endpoints

## Tech Stack
- Django
- Django REST Framework
- SQLite
- Requests

## Setup (Local)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Base URL: `http://127.0.0.1:8000`

## Docker
```bash
docker-compose up --build
```

## API Endpoints
- `GET /api/health/`
- `GET /api/projects/`
- `POST /api/projects/`
- `GET /api/projects/{project_id}/`
- `PATCH /api/projects/{project_id}/`
- `DELETE /api/projects/{project_id}/`
- `GET /api/projects/{project_id}/places/`
- `POST /api/projects/{project_id}/places/`
- `GET /api/projects/{project_id}/places/{place_id}/`
- `PATCH /api/projects/{project_id}/places/{place_id}/`

## Authentication
Use Basic Auth with Django user credentials in Postman.

## Third-Party API
Place validation uses:
- `GET https://api.artic.edu/api/v1/artworks/{external_id}`

## Postman Collection
- `postman/travel-planner.postman_collection.json`

## Useful Commands
```bash
make migrate
make runserver
make test
make lint
make format
make coverage
```
