class ParseException(BaseException):
    pass


class ApiException(BaseException):
    pass


class InternalClientException(BaseException):
    pass


class HttpException(BaseException):
    pass


class NoTokenException(BaseException):
    pass
