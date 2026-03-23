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
- Автоматический перезапуск приложения
- В продакшен-среде приложение запускается с использованием Gunicorn
- Автоматический деплой (CI/CD)

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
2. Создайте файл окружения на основе шаблона .env.sample.

### Пример файла .env.sample
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
3. Откройте файл .env и заполните необходимые переменные:
```
SECRET_KEY=your_secret_key
POSTGRES_DB=habittracker
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgras_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
TELEGRAM_TOKEN=your_token
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```
4. Соберите и запустите контейнеры:
```
docker compose up --build
```
5. Примените миграции:
```
docker compose exec web python manage.py migrate
```
6. Создайте суперпользователя:
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

После запуска проекта
```
docker compose up -d --build
```
убедитесь что все сервисы работают корректно:

1. "web" - Django сервер

Откройте в браузере http://localhost:8000/swagger/
Если страница открывается - сервис работает

Проверка через логи
```
docker compose logs -f web
```
2. "db" - PostgreSQL

Проверка подключения к базе:
```
docker compose exec db psql -U postgres
```
Если удалось войти в консоль PostgreSQL - база работает

Проверка таблиц:
```
\dt
```
3. "redis"

Проверка через CLI:
```
docker compose exec redis redis-cli
```
Внутри выполнить
```
ping
```
Ожидаемый ответ:
```
PONG
```
4. "celery" - Celery Worker

Проверка логов:
```
docker compose logs -f celery
```
Ожидаемо увидеть:
 - подключение к Redis
 - (Task received)

5. "celery-beat"

Проверка логов:
```
docker compose logs -f celery-beat
```
Ожидаемо увидеть:
 - отправку периодических задач
 - сообщение вида
```
Scheduler: Sending due task
```
6. Проверка отправки уведомлений
 - Создайте привычку с временем, близким к текущему
 - Дождитесь выполнения задачи
 - Убедитесь, что в логах Celery есть выполнения задачи 
 - Убедитесь, что в Telegram пришло сообщение

## Настройка сервера:

1. Подключитесь к серверу.
```
ssh user@server_ip
```
2. Установите Docker.
```
sudo apt update
sudo apt install docker.io docker-compose -y
```
3. Клонируйте проект.
```
git clone <repo_url>
cd project
```
4. Создайте ".env"
5. Запустите
```
docker compose up --build
```
## Автоматический деплой (CI/CD)

В проекте настроен GitHab Actions workflow для автоматической проверки и деплоя приложения.

### Как работает workflow

При каждом push в ветку develop выплоняются следующие шаги:

1. Запускается литер (flake8)
2. Запускаются тесты Django
3. Собирается Docker-образ
4. Выполняется деплой на удаленный сервер через SSH

Если тесты выполняются с ошибкой - деплой НЕ выполняется

### Необходимые Secrets в GitHub

В репозитории необходимо добавить следующие переменные:

- SERVER_IP - IP-адрес сервера
- SSH_USER - пользователь сервера
- SSH_KEY - приватный SSH-ключ
- DEPLOY_DIR - директория проекта на сервере

### Как происходит деплой

GitHab Actions подключается к серверу SSH и выполняет команды:
```
cd/home/user/project
git pull
docker compose down
docker compose up -d --build
```
### Как запускать деплой

1. Закомитте изменения:
```
git add .
git commit -m "update"
git push origin main
```
2. Перейдите во вкладку "Actions" в GitHub
3. Убедитесь, что workflow успешно выполнен

После успешного выполнения приложение автоматически обновится на сервере.
## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE).