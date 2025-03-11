# Проект ФУДГРАМ

### Бэкенд на питоне 3.11 c использованием библиотеки DRF, фронтенд React, запуск через Docker.





https://foodgramprod.hopto.org 
Тестовая версия
<br>
Логин `admin@admin.com`
Пароль `admin`


`cd infra`

`сделать копию .env файла в infra .example.env -> .env и добавить в ALLOWED_HOSTS свой домен или ip `

`docker compose up`

`docker compose exec backend python manage.py migrate`

`docker compose exec backend python manage.py collectstatic --noinput`

`docker compose exec backend python manage.py add_tags "../data/tags.json"`

`docker compose exec backend python manage.py add_ingr "../data/ingredients.json"`

Будет доступен на localhost:8000




#### Автор https://github.com/konfuzer/ 
#### Ivan Artemov
