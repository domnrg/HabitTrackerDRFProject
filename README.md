# HabitTracker DRF Project

Учебный проект для управления привычками с Django REST Framework

## Возможности
- Регистрация и аутентификация пользователей
- Создание, редактирование и удаление привычек
- Просмотр списка привычек с пагинацией
- Получение детальной информации по каждой привычке
- Валидация привычек:
  - Проверка периодичности и длительности выполнения
  - Ограничение на сочетание приятных привычек, вознаграждений и связанных привычек
- Периодическая проверка привычек через Celery и отправка уведомлений пользователям (через Telegram)
- REST API с сериализацией через DRF
- Swagger и ReDoc документация API 
- Поддержка работы в Docker с отдельными сервисами:
  - "web" - Django сервер
  - "db" - PostgreSQL
  - "redis" - Redis для очередей
  - "celery" - Celery Worker
  - "celery-beat" - планировщик периодических задач

## Технологии
- Python 3.10+
- Django 5.x
- Djangorestframework 3.16+
- Redis 7.x
- Celery 5.6+
- Celery-beat 2.8+
- Docker 24.x
- Docker Compose 2.x

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/username/HabitTrackerDRFProject.git
```
2. Создайте .env файл со следующими параметрами:
```
SECRET_KEY=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
TELEGRAM_TOKEN=
CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
```
2. Соберите и запустите контейнеры:
```
docker compose up --build
```
3. Примените миграции:
```
docker compose exec web python manage.py migrate
```
4. Создайте суперпользователя:
```
docker compose exec web python manage.py createsuperuser
```
## Доступ к сервисам:

Перейти в браузере:

Главная старница: http://localhost:8000/
Админка: http://localhost:8000/admin/
Swagger документация: http://localhost:8000/swagger/
ReDoc документация: http://localhost:8000/redoc/

## Проверка работоспособности:

1. Открыть Swagger или Redoc в браузере и проверить доступность API
2. Создать привычку через API и убедиться что она сохраняется в базе
3. Проверить логи Celery Worker - сообщение о выполнении задачи должно появляться
4. Проверить что Redis PostgreSQL доступны из контейнеров 
(docker compose exec web ping db и docker compose exec web redis-cli ping)

## Команды полезные при работе:

- Остановить контейнеры:
```
docker compose down
```
- Пересобрать контейнеры после изменений:
```
docker compose up --build
```
- Посмотреть веб-логи сервиса:
```
docker compose logs -f web
```
- Посмотреть логи Celery Worker:
```
docker compose logs -f celery
```
## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE).