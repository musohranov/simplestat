"""
Механизм хранения результатов.
Хранение происходит в sqlite БД посредством orm peewee
"""

from datetime import datetime
import peewee


class ResultStorage:
    """
    Хранилище данных.
    """

    CACHE_LIMIT = 1
    """
    Размер кэша данных, при котором происходит запись в БД
    """

    _db = None
    """
    Экземпляр orm класса доступа к БД
    """

    def __init__(self, tbl_name: str, values: dict):
        """
        :param tbl_name: Имя таблицы.
        :param values: Значения. Ключом является имя поля, значением тип.
        """

        self._cache_list = []

        #
        # Сформировать таблицу результатов
        #
        class Table(peewee.Model):
            """
            Таблица хранения результатов.
            Зарезервированное поле timestamp (primary key)
            """

            FIELD_TYPE = {
                'int': peewee.IntegerField,
                'float': peewee.FloatField,
            }
            """
            Схема поддерживаемых типов
            """

            timestamp = peewee.DateTimeField(primary_key=True)

            class Meta:
                database = self._db
                table_name = tbl_name

        self._table = Table
        for fld_name, fld_type in values.items():
            self._table._meta.add_field(fld_name, Table.FIELD_TYPE[fld_type]())

        self._db.create_tables([self._table])

    def save(self, data: dict):
        """
        Сохранить данные.
        :param data: Данные. Должны соответствовать ранее сохраненным данным
        """

        values = data.copy()
        values['timestamp'] = datetime.now()

        self._cache_list.append(values)

        if len(self._cache_list) == self.CACHE_LIMIT:
            self._table.insert_many(self._cache_list).execute()
            self._cache_list = []

    @classmethod
    def init_database(cls, file_path: str):
        """
        Инициализация БД результата
        :param file_path: Имя файла БД формата sqlite
        """

        if cls._db is not None:
            raise Exception('БД уже проинициализирована!')

        cls._db = peewee.SqliteDatabase(file_path, pragmas={
            'journal_mode': 'wal',
            'cache_size': - 1 * 64000,  # 64MB
            'foreign_keys': 1,
            'ignore_check_constraints': 0,
            'synchronous': 0})

        cls._db.connect()
