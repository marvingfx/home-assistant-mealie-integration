from __future__ import annotations

from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientError

from .exception import HttpException
from .model.model import Response, Status


class HttpClient:
    def __init__(self, client_session: ClientSession) -> None:
        self._client = client_session

    async def get(self, url: str, headers: Mapping[str, str]) -> Response:
        try:
            async with self._client.get(url=url, headers=headers) as resp:
                status = Status.SUCCESS if resp.ok else Status.FAILURE
                status_code = resp.status
                data = await resp.json()
                return Response(status=status, status_code=status_code, data=data)
        except ClientError:
            raise HttpException()

    async def post(
        self, url: str, headers: Mapping[str, str], data: Mapping[str, str]
    ) -> Response:
        try:
            async with self._client.post(url=url, data=data, headers=headers) as resp:
                status = Status.SUCCESS if resp.ok else Status.FAILURE
                status_code = resp.status
                data = await resp.json()
                return Response(status=status, status_code=status_code, data=data)
        except ClientError:
            raise HttpException()

    async def put(
        self, url: str, headers: Mapping[str, str], data: Mapping[str, str]
    ) -> Response:
        try:
            async with self._client.put(url=url, data=data, headers=headers) as resp:
                status = Status.SUCCESS if resp.ok else Status.FAILURE
                status_code = resp.status
                data = await resp.json()
                return Response(status=status, status_code=status_code, data=data)
        except ClientError:
            raise HttpException()

    async def delete(self, url: str, headers: Mapping[str, str]) -> Response:
        pass
