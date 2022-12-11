# Домашнее задание:
Написать Q&A сайт, аналог stackoverflow.com. Это будет Django приложение, 
покрытое тестами и для которого (опционально) реализовано API
Цель задания: получить навык создания веб-приложений и использования фреймворков.
Критерии успеха: задание
обязательно
, критерием успеха является работающий согласно заданию код, который 
проходит тесты, для которого проверено соответствие pep8, написана 
минимальная документация с примерами запуска.
Также проект должен разворачиваться одним из способов, описанных в секции 
Deploy. Далее успешность определяется code review.

# Настройка
## Установка 
### Локально:
pip install -r requirements.txt
выполнить миграции в скрипте /web/start
Установить postgres
пароль задаётся при первом запуске pgadmin

#### Запуск
python manage.py runserver 8000
c более подробной отладкой
python manage.py runserver_plus 8000

### Docker Compose
#### Запуск
Создал папку /home/artem/pg2 (смотри gru5.yml)
В файле ```db\docker-entrypoint-initdb.d\first_table.sql```
нужно придумать свой пароль ```
CREATE USER grusha WITH ENCRYPTED PASSWORD 'xxx';```
вместо 'xxx'

после этого выполнить 
make prod
или
make up
если пересобирать билд не надо. То есть уже выполнялась команда
make prod
и после этого код не менялся.

p.s.
В докере возможно использовать
command: uwsgi --plugin http,python3 --http :8000 --wsgi-file askme/wsgi.py --master
вместо 
command: /bin/sh start
но в этом случае не применяются миграции. Короче это запасной способ запуска.

#### Остановка
docker-compose -f gru5.yml down

#### Подключение
docker ps -a
docker exec -ti 89b014470cef /bin/sh
docker exec -u postgres -ti 5201de479d3d /bin/bash
docker exec -u postgres -ti ea95146c75f8 psql

#### Удаление
docker rmi $(docker images -q -f dangling=true)
##### остановленные контейнеров
docker system prune -a

## тесты
Для прогона тестов я выполнил```
ALTER USER grusha CREATEDB;```
где grusha имя пользователя в setting.py
Запуск тестов:
python manage.py test

# .env
рядом с readme.md нужно создать файл .env
содержащий:
```
DEBUG=True
SECRET_KEY='django-insecure-xxx'
я не пользовался, но для генерации ключа предлагают сайт https://djecrety.ir/
PG_HOST=db
PG_PORT=5432
POSTGRES_DB='askme'
POSTGRES_USER='grusha'
POSTGRES_PASSWORD='xxx'
EMAIL_FROM='xxx@inbox.ru'
EMAIL_HOST='smtp.mail.ru'
EMAIL_HOST_USER='xxx@inbox.ru'
EMAIL_HOST_PASSWORD='xxx'
EMAIL_PORT=587
ALLOWED_HOSTS=*
```
Для запуска на локальной машине
PG_HOST=localhost
ALLOWED_HOSTS="localhost","0.0.0.0","127.0.0.1"
- можно значения указывать через запятую

# Замечания
Это первый мой проект на Django. Можно сказать MVP.
Поэтому перечислю те проблемы которые уже заметил.
1. .env 
DEBUG = False не работает 
просто удалите DEBUG из env
фиксить не стал так как нашёл workaround
2. тэги должны быть уникальны 
3. кнопки like при щелчке счётчик меняется только при обновлении страницы
4. сделать тесты для api 
5. поиск не делается по содержимому (сейчас делается только по title)
6. масштабирование (redis) сейчас проект работает напрямую с postgres
то есть большие нагрузки может не выдержать
7. web/start возможно git при коммите заменил переводы строк на window. Если это так это потребуется исправить.


# requirements.txt
## create
pip freeze > requirements.txt
## use
pip install -r requirements.txt

# code style
## isort
python -m pip install isort
### run 
isort .
## mypy
python -m pip install mypy
### run 
mypy .
## flake8
python -m pip install flake8
### run
flake8
## code coverage
pip install coverage
### run
coverage run C:\Users\agrusha\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\behave\__main__.py
в файле .coveragerc нужно указать исходники