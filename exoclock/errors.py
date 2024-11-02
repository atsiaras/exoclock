
class ExoClockError(BaseException):
    pass


class ExoClockLibraryError(ExoClockError):
    pass


class ExoClockFileError(ExoClockError):
    pass


class ExoClockProcessError(ExoClockError):
    pass


class ExoClockInputError(ExoClockError):
    pass
