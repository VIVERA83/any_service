from base.base_exception import ExceptionBase


class InvalidFileTypeException(ExceptionBase):
    args = ("Ошибка валидации типа файла. Поддерживаемые типы: .jpg, .png, .gif.",)


class NotSupportedFileTypeException(ExceptionBase):
    args = ("Неподдерживаемый тип файла.",)


class TooLargeFileException(ExceptionBase):
    args = ("Файл слишком большой.",)


class EmptyFileException(ExceptionBase):
    args = ("Файл пустой, либо не был загружен.",)
