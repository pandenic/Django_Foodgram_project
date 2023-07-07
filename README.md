Service URL: pandenic.ddns.net (accessable for short period until 10 july 2023)

# Description
Website "Foodgram". On this service users are able to publish recipes, subscribe to other users' publications, add their favorite recipes to the "Favorites" list, and download a summary of products to buy in a store.

# Installation

1. Run backend as a separate api app.

Create venv
```bash
python3.9 -m venv venv
```

Install requirements
```bash
pip install -r requirements.txt
```

[Install](https://docs.docker.com/engine/install/ubuntu/) docker (linux):
```bash
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
```

Create a postgres database using "docker-compose.dev.db.yml" from "infra/" dir:
```bash
docker compose -f docker-compose.dev.db.yml up -d --build
```

Make .env file in "./backend/" dir and define variables:
```python
DEBUG=False
SECRET_KEY=(your secret key)
ALLOWED_HOSTS=(list of allowed hosts splited with space)
DB_ENGINE=django.db.backends.postgresql
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=foodgram_postgres
DB_HOST=localhost
DB_PORT=5432
```

Uncomment strings in the beginning of a "./foodgram/settings.py" file:
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

2. Run app using docker compose:

Run "docker-compose.dev.yml" from "infra/" dir:
```bash
docker compose -f docker-compose.dev.yml up -d --build
```

# Request examples
Examples showed for host "localhost".

Request documentation build using redoc:
http://localhost/api/docs/redoc.html


Sign up as a new user:
```http request
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
```http request
POST http://localhost/api/auth/token/login/
Content-Type: application/json

{
"password": "string",
"email": "string"
}
```

Get recipes list
```http request
GET http://localhost/api/recipes/
```

Create a recipe
```http request
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
