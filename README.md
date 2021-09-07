# OTUServer
Веб-сервер, частично реализующий протоĸол HTTP.

### Архитектура

Сервер реализован с использованием асинхронной архитектуры. Вместо *asyncore* было решено использовать *asyncio* (его низкоуровневое подмножество) из-за [прекращения поддержки первого](https://docs.python.org/3/library/asyncore.html). Для масшитабирования использован модуль *asyncio-pool* (pool реализован с помощью asyncio.Semaphore).

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
    Server Hostname:        localhost
    Server Port:            8080

    Document Path:          /httptest/dir2/
    Document Length:        34 bytes

    Concurrency Level:      100
    Time taken for tests:   25.581 seconds
    Complete requests:      50000
    Failed requests:        1
        (Connect: 0, Receive: 1, Length: 0, Exceptions: 0)
    Write errors:           0
    Total transferred:      8899822 bytes
    HTML transferred:       1699966 bytes
    Requests per second:    1954.58 [#/sec] (mean)
    Time per request:       51.162 [ms] (mean)
    Time per request:       0.512 [ms] (mean, across all concurrent requests)
    Transfer rate:          339.75 [Kbytes/sec] received

    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0   43 311.2      0   15000
    Processing:     0    7  56.9      5    3412
    Waiting:        0    7  56.9      5    3412
    Total:          0   50 327.1      5   15006

    Percentage of the requests served within a certain time (ms)
        50%      5
        66%      5
        75%      5
        80%      5
        90%      6
        95%      7
        98%   1005
        99%   1006
        100%  15006 (longest request)


## Требования
- Python >= 3.6
- asyncio-pool >= 0.5.2
