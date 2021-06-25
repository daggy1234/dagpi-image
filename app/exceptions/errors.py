class DagpiException(Exception):
    def __init__(self, text: str) -> None:
        self.text = text

    def __str__(self) -> str:
        return self.text


class BadUrl(DagpiException):
    pass


class NoImageFound(DagpiException):
    pass


class Unauthorised(DagpiException):
    pass


class RateLimit(DagpiException):
    pass


class BadImage(DagpiException):
    pass


class FileLarge(DagpiException):
    pass


class ServerTimeout(DagpiException):
    pass


class ManipulationError(DagpiException):
    pass


class ParameterError(DagpiException):
    pass
