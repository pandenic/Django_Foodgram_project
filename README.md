Service URL: pandenic.ddns.net (accessible for a short period until 10 July 2023)

# Description
Website "Foodgram". On this service, users are able to publish recipes, subscribe to other users' publications, add their favorite recipes to the "Favorites" list, and download a summary of products to buy in a store.

# Technologies

| Technologies | Links |
| ---- | ---- |
| ![git_Django](https://github.com/pandenic/Foodgram_project/assets/114985447/87a6dd6e-127f-47e7-bbd4-a6c28fcddf76) | [Django](https://www.djangoproject.com/) |
| ![git_DRF](https://github.com/pandenic/Foodgram_project/assets/114985447/7675ed9d-a3a3-4570-8ce1-ccbf68f37e80) | [Django REST Framework](https://www.django-rest-framework.org/) |
| ![git_Docker](https://github.com/pandenic/Foodgram_project/assets/114985447/f0c3af66-8353-4cd6-a319-d20f0e526468) | [Docker](https://www.docker.com/)
| ![git_DockerCompose](https://github.com/pandenic/Foodgram_project/assets/114985447/f5bd3ab1-09d8-4b90-9e49-22e9204a4220) | [Docker Compose](https://docs.docker.com/compose/)
| ![git_Gunicorn](https://github.com/pandenic/Foodgram_project/assets/114985447/2d81d016-e13a-44e9-ab97-ba2c8a07c65f) | [Gunicorn](https://gunicorn.org/)
| ![git_Nginx](https://github.com/pandenic/Foodgram_project/assets/114985447/584e5c7b-88c2-4870-b47d-6f7dce6bcc8f) | [Nginx](https://www.nginx.com/)
| ![git_GitHubActions](https://github.com/pandenic/Foodgram_project/assets/114985447/bf86ccf0-34d7-44e7-ae7d-e57f21a7e6c4) | CI/CD on [GitHub Actions](https://github.com/features/actions)
| ![git_React](https://github.com/pandenic/Foodgram_project/assets/114985447/8af3082e-5e44-42e8-a0b2-c57d596f229b) | [React](https://react.dev/)

# Installation

1. Run the backend as a separate API app.

Create venv
```bash
python3.9 -m venv venv
```

Install requirements
```bash
pip install -r requirements.txt
```

[Install](https://docs.docker.com/engine/install/ubuntu/) docker (Linux):
```bash
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
```

Create a Postgres database using "docker-compose.dev.db.yml" from "infra/" dir:
```bash
docker compose -f docker-compose.dev.db.yml up -d --build
```

Make .env file in "./backend/" dir and define variables:
```python
DEBUG=False
SECRET_KEY=(your secret key)
ALLOWED_HOSTS=(list of allowed hosts split with space)
DB_ENGINE=django.db.backends.postgresql
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=foodgram_postgres
DB_HOST=localhost
DB_PORT=5432
```

Uncomment strings at the beginning of a "./foodgram/settings.py" file:
```python
sfrom dotenv import load_dotenv
load_dotenv()
```

Make migrations
```bash
python manage.py migrate
```

Run backend app:
```bash
python ./backend/manage.py runserver
```

2. Run the app using docker-compose:

Run "docker-compose.dev.yml" from "infra/" dir:
```bash
docker compose -f docker-compose.dev.yml up -d --build
```

# Request examples
Examples are shown for the host "localhost".

Request documentation built using reDOC:
http://localhost/api/docs/redoc.html


Sign up as a new user:
```HTTP request
POST http://localhost/api/users/
Content-Type: application/json

{
"email": "vpupkin@yandex.ru",
"username": "vasya.pupkin",
"first_name": "Вася",
"last_name": "Пупкин",
"password": "Qwerty123"
}
```

Get token authorization:
```HTTP request
POST http://localhost/api/auth/token/login/
Content-Type: application/json

{
"password": "string",
"email": "string"
}
```

Get recipes list
```HTTP request
GET http://localhost/api/recipes/
```

Create a recipe
```HTTP request
POST http://localhost/api/recipes/
Authorization: Token <token> 
Content-Type: application/json

{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
