from urllib.parse import urlencode

import aiohttp
from starlette.responses import StreamingResponse

from base.base_accessor import BaseAccessor
from core.settings import S3Settings
from icecream import ic


class S3Accessor(BaseAccessor):
    BASE_PATH: str = "127.0.0.1"
    settings: S3Settings = None

    async def connect(self):
        self.settings = S3Settings()
        self.BASE_PATH = f"http://{self.settings.s3_host}:{self.settings.s3_port}/"

    @staticmethod
    def session() -> aiohttp.ClientSession:
        return aiohttp.ClientSession()

    def __create_url(self, method: str, **kwargs) -> str:
        """Create url from base url and params.

        Args:
            method (str): telegram API method
            kwargs: url parameters

        Return:
            object: url object
        """
        if kwargs:
            return "?".join([self.BASE_PATH + method, urlencode(kwargs)])
        return self.BASE_PATH + method

    @staticmethod
    def __create_form_data(filename: str, file_content: bytes) -> aiohttp.FormData:
        data = aiohttp.FormData()
        content_type = "application/octet-stream"
        data.add_field(
            name="file",
            value=file_content,
            filename=filename,
            content_type=content_type,
        )
        return data

    async def upload(self, filename: str, file_content: bytes):
        async with self.session() as session:
            async with session.post(
                    url=ic(self.__create_url("upload")),
                    data=self.__create_form_data(filename, file_content),
            ):
                await session.close()

    async def download(self, meme_id: str):
        session = self.session()
        response = await session.post(url=self.__create_url("download", meme_id=meme_id))

        async def stream_iterator():
            async for chunk in response.content:
                yield chunk
            await session.close()

        return StreamingResponse(
            content=stream_iterator(),
            headers=self._create_headers(meme_id + ".jpg"),
        )

    @staticmethod
    def _create_headers(filename: str) -> dict:
        return {
            "Content-Disposition": f"attachment filename={filename}",
            "Content-type": "image/jpeg",
        }
