# Travel Planner API

Django + DRF backend for travel projects and places.

## Stack
- Django
- Django REST Framework
- SQLite

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
 
## Docker
```bash
docker-compose up --build
```

## Auth
Use Basic Auth (Django user credentials).

## API (current V0.1)
- `GET /api/health/`

## Notes
This is the initial skeleton version.
Business models, CRUD endpoints, Art Institute API integration, and full validation will be added in next versions.
