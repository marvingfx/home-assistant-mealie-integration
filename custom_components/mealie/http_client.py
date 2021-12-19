from __future__ import annotations

from types import TracebackType
from typing import Mapping, Optional, Type

import aiohttp
from aiohttp.client_exceptions import ClientError

from custom_components.mealie.exception import HttpException
from custom_components.mealie.model.model import Response, Status


class HttpClient:
    def __init__(self) -> None:
        self._client: aiohttp.ClientSession = aiohttp.ClientSession()

    async def close(self) -> None:
        return await self._client.close()

    async def __aenter__(self) -> HttpClient:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        await self.close()
        return None

    async def get(self, url: str, headers: Mapping[str, str]) -> Response:
        try:
            async with self._client.get(url=url, headers=headers) as resp:
                status = Status.SUCCESS if resp.ok else Status.FAILURE
                status_code = resp.status
                data = await resp.json()
                return Response(
                    status=status, status_code=status_code, data=data
                )
        except ClientError:
            raise HttpException()

    async def post(
        self, url: str, headers: Mapping[str, str], data: Mapping[str, str]
    ) -> Response:
        try:
            async with self._client.post(
                url=url, data=data, headers=headers
            ) as resp:
                status = Status.SUCCESS if resp.ok else Status.FAILURE
                status_code = resp.status
                data = await resp.json()
                return Response(
                    status=status, status_code=status_code, data=data
                )
        except ClientError:
            raise HttpException()

    async def put(
        self, url: str, headers: Mapping[str, str], data: Mapping[str, str]
    ) -> Response:
        try:
            async with self._client.put(
                url=url, data=data, headers=headers
            ) as resp:
                status = Status.SUCCESS if resp.ok else Status.FAILURE
                status_code = resp.status
                data = await resp.json()
                return Response(
                    status=status, status_code=status_code, data=data
                )
        except ClientError:
            raise HttpException()

    async def delete(self, url: str, headers: Mapping[str, str]) -> Response:
        pass
