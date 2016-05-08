# coding: utf-8

import json
import os

from .base import BaseBackend


class JsonBackend(BaseBackend):
    """JsonBackend class that saves data to local `.json` files.

    All data are stored in separate files according their type,
    like `films.json`, `people.json` etc under a directory.

    :param location: the directory to store data. This has to be
        an absolute path. Otherwise ValueError will be raised.
    """
    def __init__(self, location=None):

        self.basedir = location

    def save(self, filename, obj):
        if not filename.endswith('json'):
            filename += '.json'

        with open(os.path.join(self.basedir, filename), "a+") as f:
            f.write(json.dumps(obj))
            f.write('\n')