# Winch

Инструмент, чтобы один раз описать HTTP API как операции Python и вызывать их из бизнес-логики, не уходя в HTTP. Класс операции — метод внешнего API, имя в проекте — экземпляр, вызов `get_user(...)` — обычная функция. Клиент держит адаптер, базу URL и секреты; в вызов его не передают. Транспорт (`httpx`, `requests`) ставите сами: Winch даёт адаптеры, без библиотеки — `ImportError` при создании адаптера.

## REST: пользователь GitHub

Слот path: аргумент вызова становится сегментом URL. Ключ не нужен.

```python
from http import HTTPMethod

from winch import Client, HttpxAdapter, Path, RestOperation


class GetUser(RestOperation):
    method = HTTPMethod.GET
    path = '/users/{username}'
    username: Path[str]


get_user = GetUser(
    client=Client(
        http_transport=HttpxAdapter(),
        base_url='https://api.github.com',
    ),
)

print(get_user(username='octocat')['login'])
```

Тот же класс с async-клиентом:

```python
import asyncio
from http import HTTPMethod

from winch import AsyncClient, AsyncHttpxAdapter, Path, RestOperation


class GetUser(RestOperation):
    method = HTTPMethod.GET
    path = '/users/{username}'
    username: Path[str]


get_user = GetUser(
    client=AsyncClient(
        http_transport=AsyncHttpxAdapter(),
        base_url='https://api.github.com',
    ),
)

print(asyncio.run(get_user(username='octocat'))['login'])
```

Для `requests` — тот же клиент, но `RequestsAdapter` (только sync).

## REST: картинка дня NASA

Слот query. Секрет — дефолт экземпляра, не аргумент вызова. `DEMO_KEY` годится, чтобы сразу увидеть ответ; свой ключ с [api.nasa.gov](https://api.nasa.gov/) подставьте так же.

```python
from http import HTTPMethod

from winch import Client, HttpxAdapter, Query, RestOperation


class GetApod(RestOperation):
    method = HTTPMethod.GET
    path = '/planetary/apod'
    api_key: Query[str]


get_apod = GetApod(
    client=Client(
        http_transport=HttpxAdapter(),
        base_url='https://api.nasa.gov',
    ),
    api_key='DEMO_KEY',
)

apod = get_apod()
print(apod['title'], apod['url'])
```

## RPC: Telegram

Имя процедуры в URL, аргументы в JSON-теле, глагол POST. Токен — на клиенте (`base_url`), не в `__call__`.

```python
import os

from winch import Client, HttpxAdapter, RpcOperation

telegram = Client(
    http_transport=HttpxAdapter(),
    base_url=(
        'https://api.telegram.org/bot'
        f'{os.environ["TELEGRAM_BOT_TOKEN"]}'
    ),
)


class GetMe(RpcOperation):
    path = '/getMe'


class SendMessage(RpcOperation):
    path = '/sendMessage'


get_me = GetMe(client=telegram)
send_message = SendMessage(client=telegram)

print(get_me())
print(send_message(chat_id=os.environ['TELEGRAM_CHAT_ID'], text='hello'))
```

## Ошибки ответа

Статус вне успешных (по умолчанию не 2xx) — **`WinchHttpException`**: в исключении весь ответ. Отказ в теле при 2xx сам по себе не ошибка Winch; автор операции решает в `read_document`.

Несуществующий пользователь GitHub:

```python
from http import HTTPMethod

from winch import (
    Client,
    HttpxAdapter,
    Path,
    RestOperation,
    WinchHttpException,
)


class GetUser(RestOperation):
    method = HTTPMethod.GET
    path = '/users/{username}'
    username: Path[str]


get_user = GetUser(
    client=Client(
        http_transport=HttpxAdapter(),
        base_url='https://api.github.com',
    ),
)

try:
    get_user(username='winch-demo-no-such-user')
except WinchHttpException as http_error:
    print(http_error.http_response.status)
    print(http_error.http_response.body)
```

Telegram при `ok: false` в теле (если статус успешный) — исключение из описания операции:

```python
import os

from winch import (
    Client,
    HttpResponse,
    HttpxAdapter,
    RpcOperation,
    WinchHttpException,
    WinchRefusalException,
)


class TelegramOperation(RpcOperation):
    def read_document(
        self,
        document: object,
        http_response: HttpResponse,
    ) -> object:
        if not isinstance(document, dict):
            return document
        if document.get('ok') is not False:
            return document
        raise WinchRefusalException(
            message=str(document.get('description', '')),
            code=document.get('error_code', 0),
            http_response=http_response,
        )


class SendMessage(TelegramOperation):
    path = '/sendMessage'


send_message = SendMessage(
    client=Client(
        http_transport=HttpxAdapter(),
        base_url=(
            'https://api.telegram.org/bot'
            f'{os.environ["TELEGRAM_BOT_TOKEN"]}'
        ),
    ),
)

try:
    send_message(chat_id=0, text='hello')
except WinchRefusalException as refused:
    print(refused, refused.code)
except WinchHttpException as http_error:
    print(http_error.http_response.status, http_error.http_response.body)
```

Нужен и `WinchHttpException`: у Telegram отказ часто приходит не 2xx, тогда сработает он, а не `read_document`.

## Своя сессия

По умолчанию адаптер открывает транспорт на каждый `send`. Если пул и заголовки соединения уже есть — передайте сессию; адаптер её не закроет.

```python
from http import HTTPMethod

import httpx

from winch import Client, HttpxAdapter, Path, RestOperation


class GetUser(RestOperation):
    method = HTTPMethod.GET
    path = '/users/{username}'
    username: Path[str]


httpx_client = httpx.Client()
get_user = GetUser(
    client=Client(
        http_transport=HttpxAdapter(httpx_client=httpx_client),
        base_url='https://api.github.com',
    ),
)

print(get_user(username='octocat')['login'])
httpx_client.close()
```

Для `requests` — `RequestsAdapter(requests_session=session)`.
