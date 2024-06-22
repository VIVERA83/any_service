from base.base_exception import ExceptionBase


class MemNotFoundException(ExceptionBase):
    args = ("Mem not found in database",)
