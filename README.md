# OTUServer
Веб-сервер, частично реализующий протоĸол HTTP.

### Архитектура

Сервер реализован с использованием асинхронной архитектуры. Вместо *asyncore* было решено использовать *asyncio* из-за [прекращения поддержки первого](https://docs.python.org/3/library/asyncore.html). Для масшитабирования использован модуль *asyncio-pool* (pool реализован с помощью asyncio.Semaphore).

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

## Нагрузочное тестирование
Количество worker'ов: 5

    ab -n 50000 -c 100 -r http://localhost:8080/

### Hardware
- Intel(R) Xeon(R) CPU E5-2630 v2 @ 2.60GHz
- 1 Gb RAM
- CentOS 6

### Результаты

    Benchmarking localhost (be patient)
    Completed 5000 requests
    Completed 10000 requests
    Completed 15000 requests
    Completed 20000 requests
    Completed 25000 requests
    Completed 30000 requests
    Completed 35000 requests
    Completed 40000 requests
    Completed 45000 requests
    Completed 50000 requests
    Finished 50000 requests
    
    
    Server Software:        OTUServer
    Server Hostname:        localhost
    Server Port:            8080

    Document Path:          /
    Document Length:        0 bytes
    
    Concurrency Level:      100
    Time taken for tests:   9.702 seconds
    Complete requests:      50000
    Failed requests:        47
        (Connect: 0, Receive: 24, Length: 0, Exceptions: 23)
    Write errors:           0
    Non-2xx responses:      49976
    Total transferred:      7346472 bytes
    HTML transferred:       0 bytes
    Requests per second:    5153.79 [#/sec] (mean)
    Time per request:       19.403 [ms] (mean)
    Time per request:       0.194 [ms] (mean, across all concurrent requests)
    Transfer rate:          739.50 [Kbytes/sec] received

    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0   11 154.2      0    7000
    Processing:     0    5  76.5      2    3076
    Waiting:        0    3  39.0      2    3076
    Total:          0   16 186.9      2    7356

    Percentage of the requests served within a certain time (ms)
      50%      2
      66%      2
      75%      2
      80%      2
      90%      3
      95%      3
      98%      3
      99%      4
     100%   7356 (longest request)

## Требования
- Python >= 3.6
- asyncio-pool >= 0.5.2
