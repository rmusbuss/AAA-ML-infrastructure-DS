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
        retry_limit = 5
        while retry_limit > 0:
            try:
                response = await client.get(url, timeout=11)
                status = response.status_code
                if status // 100 == 2:
                    data = response.read()
                    observer.observe(data)
                    return
                elif status // 100 == 5:
                    retry_limit -= 1
                    time.sleep(0.1)
                    continue
                elif status // 100 == 4:
                    retry_limit = 0
                    print('Wrong data. Check the input')
            except httpx.TimeoutException:
                print("Service doesn't Respond")
                print(f'Retrying {6 - retry_limit} time')
                retry_limit -= 1
                time.sleep(0.5)
        # response.raise_for_status()
        return
        # data = response.read()

        # observer.observe(data)
        # return
        #####################
