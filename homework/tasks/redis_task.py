import redis.asyncio as aredis


class UsersByTitleStorage:
    def __init__(self):
        # добавили decode_responses=True, чтобы приходили строки вместо байтов
        self._client = aredis.StrictRedis(decode_responses=True)

    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        await self._client.aclose()

    async def save_item(self, user_id: int, title: str) -> None:
        """
        Напишите код для сохранения записей таким образом, чтобы в дальнейшем
        можно было за один запрос получить список уникальных пользователей,
        имеющих объявления с заданным заголовком.
        """
        # YOUR CODE GOES HERE
        # добавляем по ключу title значение user_id
        # если не существует словаря, то создается новый
        async with self._client.pipeline(transaction=True) as pipe:
            await (pipe.sadd(title, user_id).execute())

    async def find_users_by_title(self, title: str) -> list[int]:
        """
        Напишите код для поиска уникальных user_id, имеющих хотя бы одно объявление
        с заданным title.
        """
        # YOUR CODE GOES HERE
        # возвращаем список элементов по ключу в виде строки
        result = await self._client.smembers(title)
        # переводим элементы из строки в int, так как у нас user_id
        return list(map(int, result))
