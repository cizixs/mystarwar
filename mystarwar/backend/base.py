# coding: utf-8


class BaseBackend(object):
    """A simple base backend interface.

    All subclass must implement their own `__init__` and `save`.

    :param location: the location indicator for each backend. This can
        vary depends on the actual implementation. For example, LocalBackend
        might accept a directory, MySQL backend might accept a connection url.
    """
    def __init__(self, location=None):
        pass

    def save(self, table, obj):
        """Save document data to database."""
        pass