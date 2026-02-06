import asyncio
import uuid
from typing import Any

import httpx

from .config import settings
from .errors import (
    AuthError,
    FikenError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)

_ERROR_MAP: dict[int, type[FikenError]] = {
    400: ValidationError,
    401: AuthError,
    403: ForbiddenError,
    404: NotFoundError,
    429: RateLimitError,
}


class FikenClient:
    """Async HTTP client for the Fiken API with rate limiting and retries."""

    def __init__(self) -> None:
        self._semaphore = asyncio.Semaphore(1)
        self._last_request_time: float = 0.0
        self._http = httpx.AsyncClient(
            base_url=settings.fiken_base_url,
            headers={
                "Authorization": f"Bearer {settings.fiken_api_key}",
                "Accept": "application/json",
            },
            timeout=30.0,
        )

    async def close(self) -> None:
        await self._http.aclose()

    async def _wait_for_rate_limit(self) -> None:
        now = asyncio.get_event_loop().time()
        elapsed = now - self._last_request_time
        if elapsed < 0.25:
            await asyncio.sleep(0.25 - elapsed)

    def _raise_for_status(self, response: httpx.Response) -> None:
        if response.is_success:
            return
        status = response.status_code
        try:
            detail = response.json()
        except Exception:
            detail = response.text

        error_cls = _ERROR_MAP.get(status)
        if error_cls:
            raise error_cls(f"HTTP {status}: {detail}", status_code=status)
        if status >= 500:
            raise ServerError(f"HTTP {status}: {detail}", status_code=status)
        raise FikenError(f"HTTP {status}: {detail}", status_code=status)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
    ) -> httpx.Response:
        async with self._semaphore:
            await self._wait_for_rate_limit()
            retries = 0
            max_retries = 3
            while True:
                response = await self._http.request(
                    method,
                    path,
                    params=params,
                    json=json,
                    headers={"X-Request-ID": str(uuid.uuid4())},
                )
                self._last_request_time = asyncio.get_event_loop().time()

                if response.status_code == 429 and retries < max_retries:
                    retries += 1
                    await asyncio.sleep(2**retries * 0.5)
                    continue

                self._raise_for_status(response)
                return response

    async def get(
        self, path: str, *, params: dict[str, Any] | None = None
    ) -> Any:
        response = await self._request("GET", path, params=params)
        return response.json()

    async def get_with_pagination(
        self, path: str, *, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        response = await self._request("GET", path, params=params)
        data = response.json()
        page = response.headers.get("Fiken-Api-Page")
        page_size = response.headers.get("Fiken-Api-Page-Size")
        page_count = response.headers.get("Fiken-Api-Page-Count")
        result_count = response.headers.get("Fiken-Api-Result-Count")
        return {
            "data": data,
            "page": int(page) if page is not None else None,
            "pageSize": int(page_size) if page_size is not None else None,
            "pageCount": int(page_count) if page_count is not None else None,
            "resultCount": (
                int(result_count) if result_count is not None else None
            ),
        }

    async def post(
        self,
        path: str,
        *,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = await self._request("POST", path, json=json, params=params)
        if response.status_code == 201:
            location = response.headers.get("Location")
            if location:
                return {"location": location}
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return {"status": response.status_code}

    async def put(
        self,
        path: str,
        *,
        json: Any | None = None,
    ) -> Any:
        response = await self._request("PUT", path, json=json)
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return {"status": response.status_code}

    async def patch(
        self,
        path: str,
        *,
        json: Any | None = None,
    ) -> Any:
        response = await self._request("PATCH", path, json=json)
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return {"status": response.status_code}

    async def delete(self, path: str) -> Any:
        response = await self._request("DELETE", path)
        return {"status": response.status_code}
