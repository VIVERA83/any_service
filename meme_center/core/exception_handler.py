import traceback
from logging import Logger

from base.base_helper import HTTP_EXCEPTION, LOG_LEVEL
from httpcore import URL
from starlette import status
from starlette.responses import JSONResponse


class ExceptionHandler:
    """This class is used to handle all exceptions that occur in the application.
    It provides a standardized way to log and return errors to the user.

    Args:
        log_level (LOG_LEVEL, optional): The log level to use. Defaults to "INFO".
        is_traceback (bool, optional): To enable or not to enable backtracking in the response.
        By default, the value is set to False.
    """

    def __init__(self, log_level: LOG_LEVEL = "INFO", is_traceback: bool = False):
        self.exception = Exception("Unknown error...")
        self.level = log_level
        self.logger = Logger(__name__)
        self.message = "Unknown error..."
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.is_traceback = is_traceback
        self.real_message = ""

    def __call__(
        self,
        exception: Exception,
        url: URL,
        logger: Logger = None,
        is_traceback: bool = False,
        status_code: int = None,
    ) -> JSONResponse:
        """This method is used to handle an exception.

        Args:
            exception (Exception): The exception that was raised.
            url (URL): The URL of the request that caused the exception.
            logger (Logger, optional): The logger to use. Defaults to None.
            is_traceback (bool, optional): To enable or not to enable backtracking in the response.
            By default, the value is set to False.

        Returns:
            JSONResponse: A JSON response containing the error details.
        """
        self.exception = exception
        self.status_code = (
            status_code if status_code else status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.logger = logger
        self.is_traceback = is_traceback
        self.handler_exception()
        return self.error_response(url)

    def error_response(self, url: URL) -> JSONResponse:
        """This method is used to create an error response.

        Args:
            url (URL): The URL of the request that caused the exception.

        Returns:
            JSONResponse: A JSON response containing the error details.
        """
        content_data = {
            "detail": HTTP_EXCEPTION.get(self.status_code),
            "message": self.message,
        }
        if self.is_traceback:
            msg = traceback.format_exc()
        else:
            msg = (
                f"url={url} "
                f"exception={self.exception.__class__} "
                f"message_to_user={self.exception}"
            )
        match self.level:
            case "CRITICAL" | 50:
                msg = (
                    f" \n_____________\n "
                    f"WARNING: an error has occurred to which there is no correct response of the application."
                    f" WE NEED TO RESPOND URGENTLY"
                    f" \nExceptionHandler:  {str(self.exception)}\n"
                    f" _____________\n" + traceback.format_exc()
                )
                self.logger.critical(msg)
            case "ERROR" | 40:
                self.logger.error(msg)
            case "WARNING" | 30:
                self.logger.warning(msg)
            case _:
                self.logger.info(msg)
        self.logger.warning(self.real_message)
        return JSONResponse(content=content_data, status_code=self.status_code)

    def handler_exception(self):
        """This method is used to handle the exception.

        It sets the status code, message, and level based on the exception.
        """

        if self.exception.args:
            self.message = self.exception.args[0]
            # self.status_code = status.HTTP_400_BAD_REQUEST
        self.real_message = self.exception.__class__.__name__
        if ex := getattr(self.exception, "exception", False):
            self.real_message = (
                f"Real exception: {ex.__class__.__name__}, args={ex.args[0]}"
            )
