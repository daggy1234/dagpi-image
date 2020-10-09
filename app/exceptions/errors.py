class DagpiException(Exception):

    def __init__(self, text: str):
        self.text = text

    def __str__(self) -> str:
        return self.text


class BadUrl(Exception):
    pass


class NoImageFound(Exception):
    pass


class InvalidToken(Exception):
    pass


class RateLimit(Exception):
    pass


class BadImage(Exception):
    pass


class FileLarge(Exception):
    pass


class ServerTimeout(Exception):
    pass


class ManipulationError(Exception):
    pass


class ParameterError(DagpiException):
    pass
