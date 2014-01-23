# coding: utf-8
class PVWattsError(Exception):
    """
    Base class for PVWatts errors
    """
    def __init__(self, message):
        Exception.__init__(self, message)


class PVWattsValidationError(PVWattsError):
    """
    Validation error on request
    """
    def __init__(self, message):
        PVWattsError.__init__(self, message)
