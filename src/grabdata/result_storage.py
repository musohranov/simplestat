"""
Хранилище результатов.
"""

from datetime import datetime
import peewee


class ResultStorage:
    """
    Хранилище данных.
    """

    # Лимит строк записей
    CACHE_LIMIT = 1

    # БД результата
    _db = None

    def __init__(self, tbl_name, values):
        """
        :param str tbl_name: Имя таблицы.
        :param dict values: Значения. Ключом является имя поля, значением тип.
        """

        self._field_names = tuple(values.keys())
        self._cache_list = []

        #
        # Сформировать таблицу результатов
        #
        class Table(peewee.Model):
            """
            Таблица хранения результатов.
            """

            FIELD_TYPE = {
                'int': peewee.IntegerField,
                'float': peewee.FloatField
            }

            timestamp = peewee.DateTimeField(primary_key=True)

            class Meta:
                database = self._db
                table_name = tbl_name

        self._table = Table
        for fld_name, fld_type in values.items():
            self._table._meta.add_field(fld_name, Table.FIELD_TYPE[fld_type]())

        self._db.create_tables([self._table])

    def save(self, data):
        """
        Сохранить данные.
        :param tuple data: Данные.
        """

        values = dict(zip(self._field_names, data))
        values['timestamp'] = datetime.now()

        self._cache_list.append(values)

        if len(self._cache_list) == self.CACHE_LIMIT:
            self._table.insert_many(self._cache_list).execute()
            self._cache_list = []

    @classmethod
    def init_database(cls, file_path):
        if cls._db is not None:
            raise Exception('БД уже проинициализирована!')

        cls._db = peewee.SqliteDatabase(file_path, pragmas={
            'journal_mode': 'wal',
            'cache_size': - 1 * 64000,  # 64MB
            'foreign_keys': 1,
            'ignore_check_constraints': 0,
            'synchronous': 0})

        cls._db.connect()
