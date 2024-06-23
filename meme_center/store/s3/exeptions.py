from base.base_exception import ExceptionBase


class S3FileNotFoundException(ExceptionBase):
    args = ("Запрошенный Мем не найден в S3 сервере. Попробуйте обновить мем.",)


class S3ConnectionErrorException(ExceptionBase):
    args = ("Не удалось подключиться к S3 серверу. Повторите попытку позже.",)


class S3UnknownException(ExceptionBase):
    args = ("Неизвестная ошибка S3 сервера.",)
