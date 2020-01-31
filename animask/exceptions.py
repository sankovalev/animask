"""Exceptions"""
class CoreException(Exception):
    """
    Base exception in core.
    """


class ImreadException(CoreException):
    pass


class InvalidSizeException(CoreException):
    pass
