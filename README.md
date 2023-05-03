# Проект YaMDB
![Github actions](https://github.com/vikomsk/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Как запустить проект на боевом сервере:

Установить на сервере docker и docker-compose.
Скопировать на сервер файлы docker-compose.yaml и default.conf:
```
scp docker-compose.yaml <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/
scp default.conf <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/nginx/
```

Добавить в Sec rets на  Github следующие данные:
```
DB_ENGINE=django.db.backends.postgresql # указать, что проект работает с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД
DB_HOST=db # название сервиса БД (контейнера) 
DB_PORT=5432 # порт для подключения к БД
DOCKER_PASSWORD= # Пароль от аккаунта на DockerHub
DOCKER_USERNAME= # Username в аккаунте на DockerHub
HOST= # IP удалённого сервера
USER= # Логин на удалённом сервере
SSH_KEY= # SSH-key компьютера, с которого будет происходить подключение к удалённому серверу
PASSPHRASE= #Если для ssh используется фраза-пароль
TELEGRAM_TO= #ID пользователя в Telegram
TELEGRAM_TOKEN= #ID бота в Telegram

```


Выполнить команды:
* git add .
* git commit -m "<commit>"
* git push

После этого будут запущены процессы workflow:
* проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest
* сборка и доставка докер-образа для контейнера web на Docker Hub
* автоматический деплой проекта на боевой сервер
* отправка уведомления в Telegram о том, что процесс деплоя успешно завершился

После успешного завершения процессов workflow на боевом сервере необходимо выполнить следующие команды:
```
sudo docker-compose exec web python manage.py migrate
```
```
sudo docker-compose exec web python manage.py createsuperuser
```
```
sudo docker-compose exec web python manage.py collectstatic --no-input 
```
----