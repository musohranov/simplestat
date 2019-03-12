"""
Утилита сбора статистики.
В качестве параметра необходимо передать путь до json файла с конфигурацией.
"""

import os

import sys
import logging

import config
from result_storage import ResultStorage
from task import GrabDataTask


def run():
    """
    Запустить обработку сбора статистики.
    """

    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG
    )

    if len(sys.argv) != 2:
        logging.error('Необходимо указать файл настройки!')
        return

    file_path = sys.argv[1]
    task_cfg_list = config.get_from_file(file_path)

    if not task_cfg_list:
        logging.error('Отсутствуют задачи для запуска!')

    ResultStorage.init_database(os.path.splitext(file_path)[0] + '.sqlite')

    for task_cfg in task_cfg_list:
        try:
            GrabDataTask.create_instance(task_cfg).start()
            logging.info('Задача %s - Успешно запущена', task_cfg)
        except:
            logging.warning('Задача %s - Ошибка запуска', task_cfg)


if __name__ == '__main__':
    run()
