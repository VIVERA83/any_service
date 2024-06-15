from datetime import datetime
from typing import Any, Callable, Type, Union
from uuid import UUID

import filetype
from core.settings import FileSettings
from fastapi import File, Query
from pydantic import BaseModel, Field, GetJsonSchemaHandler, ConfigDict
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic_core.core_schema import with_info_plain_validator_function
from starlette.datastructures import UploadFile

ID: Type[UUID] = Field(
    default=UUID("1595c2fc-397a-40c9-8105-a4d2f0a33a7a"),
    description="unique indicator of meme",
)
PAGE = Query(
    ge=1,
    default=1,
    required=False,
    description="page number",
)
PAGE_SIZE = Query(
    ge=1,
    le=100,
    default=10,
    description="page size",
)


class UploadFileSchema(UploadFile):
    """
    Pydantic model for validating and parsing an incoming file upload.

    This class inherits from starlette.datastructures.UploadFile and adds
    additional validation and parsing logic.

    Raises:
        ValueError: If the incoming file is not an instance of
            starlette.datastructures.UploadFile, or if the file type is not
            supported.
    """

    @classmethod
    def validate(cls, file: File, *_) -> Any:
        """
        Validate the incoming file upload.

        This method performs the following checks:

            1. The incoming file is an instance of
               starlette.datastructures.UploadFile.
            2. The file size is less than the maximum allowed size.
            3. The file type is supported (i.e., .xlsx or .xls).

        Args:
            file (File): The incoming file upload.

        Returns:
            Any: The validated file upload.

        Raises:
            ValueError: If the file is not valid.

        """
        if not isinstance(file, UploadFile):
            raise ValueError(f"Expected UploadFile, received: {type(file)}")

        file_size = FileSettings().size
        if file.size > file_size:
            max_size = file_size // 1024 // 1024
            raise ValueError(f"Too large file to upload, maximum size {max_size} MB")

        if type_file := filetype.guess(file.file):
            if type_file.extension in ["jpg"]:
                return file
            raise ValueError(
                f"Invalid file type: {type_file.extension}. The `jpg` type is expected."
            )
        raise ValueError("Unknown file type")

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _: CoreSchema, __: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """
        Define the JSON schema for this model.

        This method overrides the default behavior of Pydantic to provide a
        custom JSON schema for this model. The schema defines the type of the
        file as a string with a binary format.

        Returns:
            JsonSchemaValue: The JSON schema for this model.

        """
        return {"type": "string", "format": "binary"}

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _: Type[Any], __r: Callable[[Any], CoreSchema]
    ) -> CoreSchema:
        """
        Define the Core schema for this model.

        This method overrides the default behavior of Pydantic to provide a
        custom Core schema for this model. The schema includes the custom
        validation method defined in the validate method.

        Returns:
            CoreSchema: The Core schema for this model.

        """
        return with_info_plain_validator_function(cls.validate)


class OkSchema(BaseModel):
    """
    Pydantic model for returning a successful status response.

    This class defines a Pydantic model for returning a successful status
    response. The model includes two fields: status, which indicates the
    status of the response (always "Ok" in this case), and message, which
    provides a brief message describing the outcome of the request.

    Attributes:
        status (str): The status of the response. Always "Ok" in this case.
        message (str): A brief message describing the outcome of the request.
    """

    status: str = "Оk"
    message: str = "The request was successful."


class MemeSchema(BaseModel):
    id: UUID
    title: str
    # image: bytes
    model_config = ConfigDict(from_attributes=True)
