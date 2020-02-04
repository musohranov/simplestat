"""
Конфигурация.

Файлом конфигурации является json, описывающий множество задач сбора статистики

{
  "<Идентификатор задачи сбора статистики>": {
    "name": "<Название задачи>",
    "data source": {
      "driver": "<Драйвер источника данных
        python
        или
        postgresql:Строка соединения с БД>",
      "script": "<SQL выражение или python модуль>",
      "values": {
        <Словарь значений, ключом является имя поля, значением тип>
      },
      "time interval": <Временной интервал (сек.) через которые идет запрос данных>
    }
  },
}
"""

import json
import logging
from typing import List, NamedTuple


class TaskDataSourceConfig(NamedTuple):
    """
    Конфигурация источника данных задачи
    """

    driver: str
    """
    Драйвер. Варианты значений:
      * 'python', script 
      * 'postgresql;строка инициализации соединения с БД через вызов psycopg2.connect' 
    """

    script: str
    """
    Скрипт. Для случая
        driver == 'python', задает имя py файла, с обязательным методом grab_data, возвращающий словарь
        driver == 'postgresql;*', задает запрос возвращающий колонки со значениями 
        
    В обоих вариантах возращающий результат приводится к словарю с соответствующими полями заданными в values.
    """

    values: dict
    """
    Схема таблицы результата. Ключ имя поля, значение тип (поддерживаемые значения см. в 
    ResultStorage::Table.FIELD_TYPE). 
    Словарь результата сохранется в виде одной записи в таблицу.
    """

    time_interval: int
    """
    Периодичность (сек.) с которой опрашивается источник знаний 
    """


class TaskConfig:
    """
    Конфигурация задачи
    """

    def __init__(self, cfg_id: str, cfg_data: dict):
        """
        :param cfg_id: Идентификатор
        :param cfg_data: Данные
        """

        self._id = cfg_id
        self._data = cfg_data

        data_source = cfg_data['data source']
        self._data_source = TaskDataSourceConfig(data_source['driver'],
                                                 data_source['script'],
                                                 data_source['values'],
                                                 data_source['time interval'])

    def __str__(self):
        return '"{}" ({})'.format(self.name, self.id)

    @property
    def id(self) -> str:
        """
        Идентификатор
        """
        return self._id

    @property
    def name(self) -> str:
        """
        Название.
        """
        return self._data['name']

    @property
    def data_source(self) -> TaskDataSourceConfig:
        """
        Исходные данные.
        """
        return self._data_source


def get_from_file(file_path: str) -> List[TaskConfig]:
    """
    Получить конфигурации из файла
    :param file_path: Путь до файла
    """

    with open(file_path, encoding='utf-8') as file:
        file_data = json.load(file)

    logging.debug('Читается файл "%s"', file_path)

    result_list = []
    for cfg_id, cfg_data in file_data.items():
        try:
            cfg = TaskConfig(cfg_id, cfg_data)
            result_list.append(cfg)

            logging.debug('Загружена конфигурация %s', cfg)
        except:
            logging.warning('При загрузке конфигурации (%s'
                            ') произошла ошибка', cfg_id)

    return result_list

