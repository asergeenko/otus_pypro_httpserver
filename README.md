# OTUServer
Веб-сервер, частично реализующий протоĸол HTTP.

### Архитектура

Сервер реализован с использованием асинхронной архитектуры. Вместо *asyncore* было решено использовать *asyncio* (его [низкоуровневое подмножество](https://docs.python.org/3/library/asyncio-llapi-index.html)) из-за [прекращения поддержки первого](https://docs.python.org/3/library/asyncore.html). Для масшитабирования использован модуль [asyncio-pool](https://github.com/gistart/asyncio-pool) (pool реализован с помощью [asyncio.Semaphore](https://docs.python.org/3/library/asyncio-sync.html#asyncio.Semaphore)).

### Возможности

- Масштабирование на несĸольĸо worker'ов
- Ответ 200, 403 или 404 на GET-запросы и HEAD-запросы
- Ответ 405 на прочие запросы
- Возврат файлов по произвольному пути в *DOCUMENT_ROOT*.
- Вызов */file.html* возвращает содержимое *DOCUMENT_ROOT/file.html*
- Возврат *index.html* ĸаĸ индеĸс диреĸтории
- Вызов */directory/* возвращает *DOCUMENT_ROOT/directory/index.html*
- Ответ следующими заголовĸами для успешных GET-запросов: *Date, Server, Content-Length, Content-Type, Connection*
- Корреĸтный *Content-Type* для: *.html, .css, .js, .jpg, .jpeg, .png, .gif, .swf*
- Понимает пробелы и *%XX* в именах файлов

## Запуск
*httpd.py [-i IP] [-p PORT] [-w WORKERS] [-r DOC_ROOT]*

### Параметры

- *IP* - хост (по умолчанию 'localhost') 

- *PORT* - номер порта для работы сервера (по умолчанию 8080)

- *WORKERS* - количество worker'ов (по умолчанию 5)

- *DOC_ROOT* - DOCUMENT_ROOT для сервера (по умолчанию ./)

## Тестирование кода
[Репозиторий](https://github.com/s-stupnikov/http-test-suite)

### Результаты

    directory index file exists ... ok
    document root escaping forbidden ... ok
    Send bad http headers ... ok
    file located in nested folders ... ok
    absent file returns 404 ... ok
    urlencoded filename ... ok
    file with two dots in name ... ok
    query string after filename ... ok
    slash after filename ... ok
    filename with spaces ... ok
    Content-Type for .css ... ok
    Content-Type for .gif ... ok
    Content-Type for .html ... ok
    Content-Type for .jpeg ... ok
    Content-Type for .jpg ... ok
    Content-Type for .js ... ok
    Content-Type for .png ... ok
    Content-Type for .swf ... ok
    head method support ... ok
    directory index file absent ... ok
    large file downloaded correctly ... ok
    post method forbidden ... ok
    Server header exists ... ok

    ----------------------------------------------------------------------
    Ran 23 tests in 2.631s

    OK


## Нагрузочное тестирование
Количество worker'ов: 30

    ab -n 50000 -c 100 -r http://localhost:8080/httptest/dir2/

### Hardware
- Intel(R) Xeon(R) CPU E5-2630 v2 @ 2.60GHz
- 1 Gb RAM
- CentOS 6

### Результаты

    Server Software:        OTUServer
    Server Hostname:        127.0.0.1
    Server Port:            8080

    Document Path:          /httptest/dir2/
    Document Length:        34 bytes

    Concurrency Level:      100
    Time taken for tests:   20.027 seconds
    Complete requests:      50000
    Failed requests:        0
    Write errors:           0
    Total transferred:      8650000 bytes
    HTML transferred:       1700000 bytes
    Requests per second:    2496.57 [#/sec] (mean)
    Time per request:       40.055 [ms] (mean)
    Time per request:       0.401 [ms] (mean, across all concurrent requests)
    Transfer rate:          421.78 [Kbytes/sec] received

    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0   33 266.8      0    7001
    Processing:     1    5  43.2      4    2646
    Waiting:        1    5  43.2      4    2646
    Total:          1   38 283.0      4    9055
        
## E2E-тестирование

Браузер: Mozilla Firefox 90.0.2 (64bit), Windows 10

Запрос: http://localhost/httptest/wikipedia_russia.html
    
### Результат

<img src="https://raw.githubusercontent.com/asergeenko/otus_pypro_httpserver/main/img/wikipedia_test_output.jpg" alt="Страница 'Russia' в Wikipedia" />


## Требования
- Python >= 3.6
- asyncio-pool >= 0.5.2
