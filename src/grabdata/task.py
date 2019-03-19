"""
Задача сбора данных.

Класс GrabDataTask является абстрактным и содержит базовый интерфейс задачи сбора статистики.
Классы наследники реализуют сбора данных из различных (python, postgresql, ...)
типов источников данных.
"""

import logging
from abc import ABC, abstractmethod
from threading import Thread
from time import sleep

import psycopg2
from psycopg2.extras import DictCursor

from result_storage import ResultStorage


class GrabDataTask(ABC, Thread):
    """
    Задача сбора данных.
    """

    def __init__(self, cfg):
        """
        :param TaskConfig cfg: Конфигурация.
        """

        super().__init__()
        self._cfg = cfg

        self._result_storage = ResultStorage(cfg.id, cfg.data_source.values)

    def run(self):
        """
        Выполнить задачу.
        """

        while True:
            sleep(self._cfg.data_source.time_interval)

            result = self._iteration()
            self._result_storage.save(result)

            logging.debug('Задача %s - Выполнена', self._cfg)

    @abstractmethod
    def _iteration(self):
        """
        Итерация сбора данных.
        """

    @staticmethod
    def create_instance(cfg):
        """
        Создать экземпляр класса задачи сбора данных.
        :param TaskConfig cfg: Конфигурация.
        :rtype: GrabDataTask
        """

        if PythonGrabDataTask.check(cfg.data_source):
            return PythonGrabDataTask(cfg)

        if PostgresqlGrabDataTask.check(cfg.data_source):
            return PostgresqlGrabDataTask(cfg)

        raise Exception('Не поддерживамый тип конфигурации: {}'.format(cfg))


class PythonGrabDataTask(GrabDataTask):
    """
    Задача сбора данных, где в качестве источника данных используется python скрипт.
    """

    @staticmethod
    def check(data_source_cfg):
        """
        Является ли исходные данные текущего типа 'python'.
        :param TaskDataSourceConfig data_source_cfg: Конфигурация исходных данных.
        :rtype: bool
        """

        return data_source_cfg.driver == 'python'

    def __init__(self, cfg):
        """
        :param TaskConfig cfg: Конфигурация.
        """
        super().__init__(cfg)

        with open(cfg.data_source.script, encoding='utf-8') as file:
            script_text = file.read()

        self._script = compile(script_text, cfg.data_source.script, 'exec')

    def _iteration(self):
        exec(self._script)
        return eval('grab_data()')


class PostgresqlGrabDataTask(GrabDataTask):
    """
    Задача сбора данных, где в качестве источника данных используется СУБД Postgresql.
    """

    @staticmethod
    def check(data_source_cfg):
        """
        Является ли исходные данные текущего типа 'postgresql'.
        :param TaskDataSourceConfig data_source_cfg: Конфигурация исходных данных.
        :rtype: bool
        """

        return data_source_cfg.driver.split(';')[0] == 'postgresql'

    def __init__(self, cfg):
        """
        :param TaskConfig cfg: Конфигурация.
        """
        super().__init__(cfg)

        self._db_connect = psycopg2.connect(cfg.data_source.driver.split(';')[1])
        self._db_cursor = self._db_connect.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def _iteration(self):
        self._db_cursor.execute(self._cfg.data_source.script)
        return dict(self._db_cursor.fetchone())
