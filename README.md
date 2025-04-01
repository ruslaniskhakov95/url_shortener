# url_shortener

## API
API сервиса URL_shortener содержит три блока: links, auth, users.
1. links - смысловая часть, содержит 6 эндпоинтов: создание короткого кода, редактирование, удаление (эти три доступны аутентифицированным пользователям), а также получение редиректа, поиск короткой ссылки по оригинальной и статистика использования.
2. auth - стандартная система аутентификации, основанная на fastapi-users с использованием JWT-токенов.
3. users - информация о пользователях из fastapi-users.

## Примеры запросов

Регистрация
<img width="1331" alt="Снимок экрана 2025-04-01 в 22 47 49" src="https://github.com/user-attachments/assets/dc1f4aaa-d1a0-49f5-9c16-6c88b6cb9b25" />

Логин
<img width="1333" alt="Снимок экрана 2025-04-01 в 22 48 53" src="https://github.com/user-attachments/assets/d054cf2b-12a2-48dc-894f-1c19be9fbaf4" />

Информация о текущем пользователе
<img width="1328" alt="Снимок экрана 2025-04-01 в 22 50 09" src="https://github.com/user-attachments/assets/a306e3a1-0aa6-44a0-b863-0c25914d6320" />

Аутентифицированное создание корткого кода
<img width="1322" alt="Снимок экрана 2025-04-01 в 22 52 26" src="https://github.com/user-attachments/assets/4a682f2e-1321-48ea-8444-1c4f606eefa6" />

Изменение кода и expiration time (можно по отдельности, также в этом же эндпоинте можно изменить и оригинальный маршрут)
<img width="1318" alt="Снимок экрана 2025-04-01 в 22 54 01" src="https://github.com/user-attachments/assets/42cc12cd-1fed-41e8-9a25-911c014bc444" />

Запрос на редирект (был выполнен два раза) - доступно неаутентифицированным пользователям
<img width="1319" alt="Снимок экрана 2025-04-01 в 22 56 15" src="https://github.com/user-attachments/assets/5537d783-43b8-4169-8400-6397ada9ff8f" />

Статистика посещений
<img width="1333" alt="Снимок экрана 2025-04-01 в 22 57 11" src="https://github.com/user-attachments/assets/ad8de7e3-3961-45e0-9193-f685844dae3b" />

## Запуск
docker compose up

## БД
1. PostgreSQL 17
2. Таблицы users и short_urls






