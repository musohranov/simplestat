# Сбор и просмотр статистики
Решение представляет из себя приложение сбора и просмотра статистики.

Приложение сбора статистки предоставляет возможность:
* На уровне файла конфигурации определять настройки сбора данных
* Сбор данных посредством python скрипта или запросом в БД postgresql (без необходимости писать хотя бы одну строку кода
)

Приложение просмотра статистики представлено в виде web сервера с возможностью просматривать данные в виде google charts

## Архитектура
### Сбор статистики
Решение выполнено в виде [консольного приложения](/src/grabdata/app.py) где на вход передается [конфигурационный файл](/src/grabdata/config.py), 
который содержит параметры сбора данных, которые в свою очередь записываются в соответствующую бд формата sqlite.  

### Просмотр статистики
Решение выполнено в виде [web сервера](/src/report/app.py) которое в качестве параметра принимает файл с данными (бд формата sqlite).
Веб сервер предоставляет возможность выбора отчета по конкретной задаче сбора данных и непосрдственно страницу отображения данных по задаче в виде google charts.    

## Пример сбора статистики
Сформируем [файл конфигурации](/example/example.json) с двумя задачами сбора данных:

* Генерация случайных чисел каждые 60 секунд
```
  "random": {
    "name": "Случайные числа",
    "data source": {
      "driver": "python",
      "script": "e:\\!SimpleStat\\examples\\test_random.py",
      "values": {
        "v1": "int",
        "v2": "int"
      },
      "time interval": 60
    }
```
_Скрипт сбора данных [test_random.py](/example/test_random.py)_

* Считывание курса крипто-валют каждые 30 секунд
```
  "crypto_currency": {
    "name": "Курс крипто-валют",
    "data source": {
      "driver": "python",
      "script": "e:\\!SimpleStat\\examples\\test_crypto_currency.py",
      "values": {
        "Bitcoin": "float",
        "Ethereum": "float",
        "Ripple": "float"
      },
      "time interval": 30
    }
  }
```
_Скрипт сбора данных [test_crypto_currency.py](/example/test_crypto_currency.py)_

Выполним команду сбора данных согласно конфигурации
```sh
python.exe /src/grabdata/app.py /examples/example.json
2020-02-05 00:14:00 DEBUG: Читается файл "e:\!SimpleStat\examples\example.json"
2020-02-05 00:14:00 DEBUG: Загружена конфигурация "Случайные числа" (random)
2020-02-05 00:14:00 DEBUG: Загружена конфигурация "Курс крипто-валют" (crypto_currency)
2020-02-05 00:14:00 DEBUG: ('CREATE TABLE IF NOT EXISTS "random" ("timestamp" DATETIME NOT NULL PRIMARY KEY, "v1" INTEGER NOT NULL, "v2" INTEGER NOT NULL)', [])
2020-02-05 00:14:00 INFO: Задача "Случайные числа" (random) - Успешно запущена
2020-02-05 00:14:00 DEBUG: ('CREATE TABLE IF NOT EXISTS "crypto_currency" ("timestamp" DATETIME NOT NULL PRIMARY KEY, "Bitcoin" REAL NOT NULL, "Ethereum" REAL NOT NULL, "Monero" REAL NOT NULL, "BitcoinCash" REAL NOT NULL, "BitcoinGold" REAL NOT NULL, "CARDANO" REAL NOT NULL, "DASH" REAL NOT NULL, "EOS" REAL NOT NULL, "IOTA" REAL NOT NULL, "NEM" REAL NOT NULL, "NEO" REAL NOT NULL, "OmiseGo" REAL NOT NULL, "Ripple" REAL NOT NULL)', [])
2020-02-05 00:14:00 INFO: Задача "Курс крипто-валют" (crypto_currency) - Успешно запущена
2020-02-05 00:14:36 DEBUG: ('INSERT INTO "crypto_currency" ("timestamp", "Bitcoin", "Ethereum", "Monero", "BitcoinCash", "BitcoinGold", "CARDANO", "DASH", "EOS", "IOTA", "NEM", "NEO", "OmiseGo", "Ripple") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [datetime.datetime(2020, 2, 5, 0, 14, 36, 940035), 9187.26, 188.39, 74.816, 379.33, 11.3, 0.05609, 110.98, 4.153, 0.3304, 0.04727, 12.265, 0.974, 0.26605])
...
```

На выходе получаем одноименный файл [бд sqlite](/example/example.sqlite) с таблицами соответствующих задач сбора данных  
![](/example/example_sqlite_tables.png)
![](/example/example_sqlite_crypto_currency.png)

## Пример просмотра статистики
Запустим web сервер
```sh
python.exe /src/report/app.py /examples/example.sqlite
```

Страница по умолчанию отображает список задач доступных для детального просмотра собранных данных
![](/example/example_webpage_task_list.png) 

Выберем страницу с данными курсов крипто-валют
![](/example/example_webpage_crypto_currency_task.png) 

_[Сгенерированная web страница](/example/example_webpage_crypto_currency_task.html)_

