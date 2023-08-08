class ParaphraserExceptions(Exception):
    def __init__(self, _message):
        super().__init__(_message)
        self._message = _message
    def __str__(self) -> str:
        return self._message

class InvalidModeError(ParaphraserExceptions):
    pass

class LanguageNotSupportedError(ParaphraserExceptions):
    pass