# test-fastapi-project

В репозитории находятся служебные файлы, FastAPI приложение в директории *src* и тесты в директории *tests*.

## Как запустить?

**1. Создание .env файла**

Перед запуском необходимо создать *.env* файл в корневой директории срипта. Файл должен содержать переменные по аналогии с *.env.example*.

**Описание переменных окружения:**

Обязательные переменные:
<ul>
  <li><em>API_PORT</em> - номер порта хоста, на котором запускается приложение</li>
  <li><em>AUTH_SECRET_KEY</em> - секретный ключ аутентификации пользователей в приложении</li>
</ul>

Опциональные переменные:
<ul>
  <li><em>ALGORITHM</em> - алгоритм хэширования (по умолчанию - HS256)</li>
  <li><em>ACCESS_TOKEN_EXPIRE_MINUTES</em> - время жизни JWT токена (в минутах, по умолчанию - 30)</li>
</ul>

**2. Запуск через docker**

Запустите файл docker-compose из корневой директории срипта.

Документация API в формате OpenAPI расположена по эндпоинту - */docs*.
# P.S.
Логирование не сделано по причине того, что проект небольшой и базовые события (получения запросов, ответы и тд.) логируются самим FastAPI. К более серьезному проекту можно было бы подключить Sentry или поднять ELK.
