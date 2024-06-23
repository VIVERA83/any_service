from base.base_exception import ExceptionBase


class MemNotFoundException(ExceptionBase):
    args = ("Мем не найден в базе данных.",)


class MemServerConnectionException(ExceptionBase):
    args = ("Не удалось подключиться к серверу данных. Повторите попытку позже.",)


class MemUnknownException(ExceptionBase):
    args = ("Неизвестная ошибка сервера данных.",)
