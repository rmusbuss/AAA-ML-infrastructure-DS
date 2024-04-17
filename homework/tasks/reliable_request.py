import abc

import httpx

import time


class ResultsObserver(abc.ABC):
    @abc.abstractmethod
    def observe(self, data: bytes) -> None: ...


async def do_reliable_request(url: str, observer: ResultsObserver) -> None:
    """
    Одна из главных проблем распределённых систем - это ненадёжность связи.

    Ваша задача заключается в том, чтобы таким образом исправить этот код, чтобы он
    умел переживать возвраты ошибок и таймауты со стороны сервера, гарантируя
    успешный запрос (в реальной жизни такая гарантия невозможна, но мы чуть упростим себе задачу).

    Все успешно полученные результаты должны регистрироваться с помощью обсёрвера.
    """

    async with httpx.AsyncClient() as client:
        # YOUR CODE GOES HERE
        # добавляем 5 ретраев, если сервер сразу не отвечает 
        # (из-за серверной ошибки)
        retry_limit = 5
        while retry_limit > 0:
            try:
                # включаем таймаут в 11 секунд (таймаут подстроен под тесты)
                response = await client.get(url, timeout=11)
                # получаем код ответа и в зависимости от типа ошибки делаем
                # определенные действия
                status = response.status_code
                # если все ок, то регистрируем рез-ты с помощью обсервера
                if status // 100 == 2:
                    data = response.read()
                    observer.observe(data)
                    return
                # если ошибка сервера пробуем еще
                elif status // 100 == 5:
                    retry_limit -= 1
                    time.sleep(0.1)
                    continue
                # если ошибка на стороне клиента, то пишем, что
                # он что-то не то передает
                elif status // 100 == 4:
                    retry_limit = 0
                    print('Wrong data. Check the input')
            # если ошибка в таймауте, то мы ретраим и печатаем
            except httpx.TimeoutException:
                print("Service doesn't Respond")
                print(f'Retrying {6 - retry_limit} time')
                retry_limit -= 1
                time.sleep(0.5)
        return
        #####################
