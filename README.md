# Foodgram - Продуктовый помощник

### _Стек технологий_
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

### _Описание проекта_
Платформа «Foodgram - Продуктовый помощник»
Это платформа для создания и публикации своих кулинарных рецептов с возможностью подписываться на других авторов, добавления их рецептов к себе в избранное, а также формирования удобного списка продуктов по избранным рецептам.

### _Сайт_
[foodgram.kravchun.ru](foodgram.kravchun.ru)

### _Документация к API_
[foodgram.kravchun.ru/api/docs](foodgram.kravchun.ru/api/docs)

### _Как запустить проект (Windows)*_ 
* Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/Loklipon/foodgram-project-react
```
```
cd foodgram-project-react
```
* В настройках проекта (settings.py) раскомментируйте DATASBASE для локального запуска, и закомментируйте DATABASE для запуска на удаленном сервере
* Создать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/Script/activate
```
* Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
* Перейти в папку foodgram-project-react, и выполнить миграции:
```
cd api_yamdb
```
```
python manage.py makemigrations
```
```
python manage.py migrate
```
* Запустить проект:
```
python3 manage.py runserver
```
*Проект будет доступен для API запросов по адресу 127.0.0.1:8000