#  Проект ФУДГРАМ 
![Cooking](https://img.shields.io/badge/Cooking-FOODGRAM%20App-orange?style=for-the-badge&logo=chef&logoColor=white)

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.1%2B-success?logo=django&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-20.1-green?logo=gunicorn)
![Djoser](https://img.shields.io/badge/Djoser-2.3-orange?logo=django)
![React](https://img.shields.io/badge/React-17-blue?logo=react)
![Nginx](https://img.shields.io/badge/Nginx-1.25-green?logo=nginx)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)
![GitHub Workflow](https://img.shields.io/badge/GitHub_Actions-CI/CD-blue?logo=githubactions)
![Flake8](https://img.shields.io/badge/code%20style-Flake8-blue?logo=python&logoColor=white)
![isort](https://img.shields.io/badge/imports-isort-%2336a9ae?style=for-the-badge)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)


Workflow:
![Build Status](https://github.com/konfuzer/foodgram/actions/workflows/main.yml/badge.svg)

# My Project


## Технологии
- **Backend:** Python/Django, DRF, Gunicorn, Djoser
- **Frontend:** Javascript/React
- **Database:** PostgreSQL
- **Server:** Nginx
- **DevOps:** Docker Compose
- **Linters Python:** Isort with plugins, Flake8, Black


## О проекте

###  Проект позволяет пользователям делиться рецептами и следить за рецептами других.


## Тестовый сайт

https://foodgramprod.hopto.org 
<br>
Логин `admin@admin.com`
Пароль `admin`



## Как развернуть локально?

Склонировать репозиторий 

`git clone https://github.com/konfuzer/foodgram.git`

Перейти в папку
 
`cd foodgram/infra`

сделать копию .env файла в infra .example.env -> .env

добавить в ALLOWED_HOSTS и CSRF_TRUSTED_ORIGINS свой домен или ip (при необходимости)

Убедиться что установлен докер https://docs.docker.com/compose/ 

Запустить команды в консоли из папки `infra` 

`docker compose up`

`docker compose exec backend python manage.py migrate`

`docker compose exec backend python manage.py collectstatic --noinput`

`docker compose exec backend python manage.py add_data`

Если всё выполнено верно сайт будет доступен в браузере по ссылке http://localhost:8000




#### Автор https://github.com/konfuzer/ 
#### Ivan Artemov
