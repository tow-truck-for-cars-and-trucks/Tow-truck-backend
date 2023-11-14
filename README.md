![TTExpress](https://github.com/tow-truck-for-cars-and-trucks/Tow-truck-backend/actions/workflows/main.yml/badge.svg)

# Проект TTExpress - эвакуатор для легковых и грузовых авто

## Описание проекта
Приложение-сервис для легковых, грузовых - машин, спецтехники и мотоциклов.

## Стек технологий
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)


### Подготовка проекта к запуску

#### `3` и `4` пункты для локального запуска

1. *Склонируйте репозиторий и перейдите в него*:

    ```sh
    git clone https://github.com/tow-truck-for-cars-and-trucks/Tow-truck-backend.git
    ```
    ```sh
    cd Tow-truck-backend/
    ```
---
2. *Для работы с PostgreSQL*:

    * Создайте в директории `src/infra/` файл `.env` командой:

        ```sh
        touch src/infra/.env
        ```
        > Заполните переменные по примеру файла `.env.example`
---
3. *Создайте и активируйте виртуальное окружение*:

    ```sh
    python -m venv venv
    ```
    - Если у вас Linux/macOS
        ```sh
        source venv/bin/activate
        ```

    - Если у вас windows
        ```sh
        source venv/scripts/activate
        ```
---
4. *Обновите pip и установите зависимости*:

    ```sh
    python -m pip install --upgrade pip
    ```
    ```sh
    pip install -r src/backend/requirements.txt
    ```

### Для локального запуска используйте инструкцию

1. *Выполните миграции*:

    * Инициализируйте миграции
        ```sh
        python src/backend/manage.py migrate
        ```

    * Создайте миграции
        ```sh
        python src/backend/manage.py makemigrations user
        ```
        ```sh
        python src/backend/manage.py makemigrations towin
        ```

    * Примените миграции
        ```sh
        python src/backend/manage.py migrate
        ```
---
2. *Создайте суперюзера*:

    ```sh
    python src/backend/manage.py createsuperuser
    ```

    > Для примера, данные суперюзера:

        username: admin
        mail: admin@admin.ru
        password: admin
        password (again): admin

---
3. *Наполните базу данными*:

    Команды для выгрузки данных из csv-файлов:

    ```sh
    python src/backend/manage.py importtd
    ```

    -    > Для удаления данных из базы есть(будет наверное) доп. опция `--delete`:

            ```sh
            python src/backend/manage.py <команда> --delete
            ```
---
4. *Соберите статику*:
    ```sh
    python src/backend/manage.py collectstatic --noinput
    ```
---
5. *Локальный запуск*:

    ```sh
    python src/backend/manage.py runserver
    ```
---

### Для запуска в Docker-контейнере используйте инструкцию

1. *Запустите сборку контейнеров*:

    ```sh
    docker compose -f src/infra/docker-compose.yaml up -d --build
    ```
2. *Для остановки контейнера*:
    ```sh
    docker compose -f src/infra/docker-compose.yaml down
    ```
---


### Команда backend

- Варачев Андрей
- Оскалов Лев
- Черный Владимир
- Алексенцев Михаил
- Чежин Руслан
