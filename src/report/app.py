"""
Вебсервер статистики.
В качестве параметра необходимо передать путь до sqlite файла с данными.

Реализованы две страницы:
 - Список задач по которым представлена статистика (страница по умолчанию)
 - Стастистика задачи в виде google charts
"""

import sys
import os

import peewee
from flask import Flask, render_template, g, current_app

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
app.config.from_object(__name__)


@app.route('/')
@app.route('/tasks')
def _tasks():
    """
    Страница со списком задач. Список задач представлен одноименными таблицами с данными, сформированными
    на этапе сбора данных
    """
    task_list = _get_db().get_tables()
    return render_template('tasks.html', **locals())


@app.route('/tasks/<task_id>')
def _task(task_id: str):
    """
    Страница статисти по задаче (в виде google charts)
    :param task_id: Идентификатор задачи
    """
    cursor = _get_db().execute_sql('''SELECT * FROM "{}"'''.format(task_id))

    # Сформировать перечень колонок со значениями, исключая pk timestamp, она будет добавлена безусловно в шаблоне
    column_list = [c[0] for c in cursor.description if c[0] not in 'timestamp']

    # Сформировать массив значений в строковом исполнении
    row_list = []
    for row in cursor.fetchall():
        row_str = tuple(map(str, row))
        row_list.append('''new Date('{}'), '''.format(row_str[0]) + ', '.join(row_str[1:]))

    return render_template('task.html', **locals())


def _get_db() -> peewee.SqliteDatabase:
    """
    Получить БД
    """

    if not hasattr(g, 'db'):
        _db = peewee.SqliteDatabase(current_app.config['DATABASE'], pragmas={
            'journal_mode': 'wal',
            'cache_size': - 1 * 64000,  # 64MB
            'foreign_keys': 1,
            'ignore_check_constraints': 0,
            'synchronous': 0})

        _db.connect()
        g.db = _db

    return g.db


def _close_db(_):
    """
    Закрыть соединение с БД
    """

    _db = g.pop('db', None)
    if _db is not None:
        _db.close()


def run():
    """
    Запустить сервер
    """

    app.config.from_mapping(
        DATABASE=sys.argv[1],
    )
    app.teardown_appcontext(_close_db)
    app.run(debug=True)


if __name__ == "__main__":
    run()
