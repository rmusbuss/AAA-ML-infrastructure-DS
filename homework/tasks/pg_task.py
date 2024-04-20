from dataclasses import dataclass

import asyncpg


@dataclass
class ItemEntry:
    item_id: int
    user_id: int
    title: str
    description: str


class ItemStorage:
    def __init__(self):
        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        # We initialize client here, because we need to connect it,
        # __init__ method doesn't support awaits.
        #
        # Pool will be configured using env variables.
        self._pool = await asyncpg.create_pool()

    async def disconnect(self) -> None:
        # Connections should be gracefully closed on app exit to avoid
        # resource leaks.
        await self._pool.close()

    async def create_tables_structure(self) -> None:
        """
        Создайте таблицу items со следующими колонками:
         item_id (int) - обязательное поле, значения должны быть уникальными
         user_id (int) - обязательное поле
         title (str) - обязательное поле
         description (str) - обязательное поле
        """
        # In production environment we will use migration tool
        # like https://github.com/pressly/goose
        # YOUR CODE GOES HERE
        # выполняем SQL запрос создания таблицы с ненулевыми полями
        await self._pool.execute('''
                CREATE TABLE items (
                    item_id bigint primary key,
                    user_id bigint not null,
                    title text not null,
                    description text not null
                );
        ''')

    async def save_items(self, items: list[ItemEntry]) -> None:
        """
        Напишите код для вставки записей в таблицу items одним запросом, цикл
        использовать нельзя.
        """
        # Don't use str-formatting, query args should be escaped to avoid
        # sql injections https://habr.com/ru/articles/148151/.
        # YOUR CODE GOES HERE
        # обозначаем поля, которые в нашей таблице
        fields = ['item_id', 'user_id', 'title',  'description']
        fields_list = []

        # итерируемся по каждой входящей строке (item)
        # и дальше по очереди по каждому полю
        for item in items:
            temp_list = []
            for field in fields:
                # вытаскиваем из ItemEntry значение из поля и помещаем в list
                temp_list.append(getattr(item, field))
            # как только по очереди по всем полям пробежались
            # переводим лист полей в tuple и его помещаем в list
            fields_list.append(tuple(temp_list))

        # и теперь помещаем список кортежей значений в таблицу
        await self._pool.executemany('''
                INSERT INTO items VALUES
                    ($1, $2, $3, $4)''',
                                     [
                                      (item.item_id,
                                       item.user_id,
                                       item.title,
                                       item.description)
                                      for item in items
                                     ])

    async def find_similar_items(
        self, user_id: int, title: str, description: str
    ) -> list[ItemEntry]:
        """
        Напишите код для поиска записей, имеющих указанные user_id, title и description.
        """
        # YOUR CODE GOES HERE
        # выполняем фильтрующий SQL запрос
        result = await self._pool.fetch('''
                SELECT * FROM items
                WHERE 1=1
                      AND user_id = $1
                      AND title = $2
                      AND description = $3
                              ''', *[user_id, title, description])
        # возвращаем ответ от БД в виде списка из ItemEntry
        return [ItemEntry(**row) for row in result]
