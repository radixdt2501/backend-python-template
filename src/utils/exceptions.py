class BaseException(Exception):
    pass


class MissingEnvironmentVariable(BaseException):
    pass


class GenerateTokenException(BaseException):
    pass


class DuplicateEntryException(BaseException):
    pass


class DatabaseException(BaseException):
    pass


class InvalidDataFormatException(BaseException):
    pass
