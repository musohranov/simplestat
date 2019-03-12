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
from collections import namedtuple


def get_from_file(file_path):
    """
    Получить конфигурации из файла.

    :param str file_path: Путь до файла.
    :rtype: list[TaskConfig]
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


class TaskConfig:
    """
    Конфигурация задачи.
    """

    def __init__(self, cfg_id, cfg_data):
        """
        :param str cfg_id: Идентификатор.
        :param cfg_data: Данные.
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
    def id(self):
        """
        Идентификатор.
        :rtype: str
        """
        return self._id

    @property
    def name(self):
        """
        Название.
        :rtype: str
        """
        return self._data['name']

    @property
    def data_source(self):
        """
        Исходные данные.
        :rtype: TaskDataSourceConfig
        """
        return self._data_source


TaskDataSourceConfig = namedtuple('TaskDataSourceConfig', ['driver',
                                                           'script',
                                                           'values',
                                                           'time_interval'])
