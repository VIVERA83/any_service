from urllib.parse import urlencode

import aiohttp

from base.base_accessor import BaseAccessor
from core.settings import S3Settings
from icecream import ic

from store.s3.exeptions import (
    S3FileNotFoundException,
    S3ConnectionErrorException,
    S3UnknownException,
)


def exception_handler(func):
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except IOError as e:
            if e.errno == 111:
                raise S3ConnectionErrorException(exception=e)
            raise S3UnknownException(exception=e)
        except S3FileNotFoundException as e:
            raise e
        except Exception as e:
            raise S3UnknownException(exception=e)

    return wrapper


class S3Accessor(BaseAccessor):
    BASE_PATH: str
    settings: S3Settings

    @exception_handler
    async def upload(self, filename: str, file_content: bytes):
        async with self.session() as session:
            async with session.post(
                url=self.__create_url("upload"),
                data=self.__create_form_data(filename, file_content),
            ):
                await session.close()

    @exception_handler
    async def download(self, meme_id: str):
        session = self.session()
        self.logger.info(self.__create_url(f"download/{meme_id}"))
        response = await session.post(url=self.__create_url(f"download/{meme_id}"))
        if response.status != 200:
            raise S3FileNotFoundException()

        async def stream_iterator():
            async for chunk in response.content:
                yield chunk
            await session.close()

        return stream_iterator()

    @exception_handler
    async def delete(self, meme_id: str):
        async with self.session() as session:
            await session.delete(url=self.__create_url(f"delete/{meme_id}"))

    async def connect(self):
        self.settings = S3Settings()
        self.BASE_PATH = f"http://{self.settings.s3_host}:{self.settings.s3_port}/"
        self.logger.info(self.BASE_PATH)
        self.logger.info(f"{self.__class__.__name__} connected")

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

    @staticmethod
    def _create_headers(filename: str) -> dict:
        return {
            "Content-Disposition": f"attachment filename={filename}",
            "Content-type": "image/jpeg",
        }
