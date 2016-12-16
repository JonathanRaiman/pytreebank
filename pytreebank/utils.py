"""
Python 3 / 2 compatibility functions.
"""
from __future__ import print_function

import os
import sys

if sys.version_info >= (3,3):
    makedirs = os.makedirs
    def normalize_string(string):
        return string.replace("\xa0", " ")\
                     .replace("\\", "")\
                     .replace("-LRB-", "(")\
                     .replace("-RRB-", ")")\
                     .replace("-LCB-", "{")\
                     .replace("-RCB-", "}")\
                     .replace("-LSB-", "[")\
                     .replace("-RSB-", "]")
    old_print = print
    def print(*args, **kwargs):
        old_print(*args, **kwargs)
    from urllib.request import urlretrieve
else:
    old_makedirs = os.makedirs
    def makedirs(path, mode=0o777, exist_ok=False):
        if not exist_ok:
            return old_makedirs(path, mode)
        else:
            if not os.path.exists(path):
                return old_makedirs(path, mode)

    def normalize_string(string):
        return string.replace(u"\xa0", " ")\
                     .replace("\\", "")\
                     .replace("-LRB-", "(")\
                     .replace("-RRB-", ")")\
                     .replace("-LCB-", "{")\
                     .replace("-RCB-", "}")\
                     .replace("-LSB-", "[")\
                     .replace("-RSB-", "]")

    old_print = print
    def print(*args, **kwargs):
        flush = kwargs.pop("flush", False)
        old_print(*args, **kwargs)
        file = kwargs.get("file", sys.stdout)
        if flush and file is not None:
            file.flush()
    from urllib import urlretrieve

__all__ = ["makedirs", "normalize_string", "urlretrieve", "print"]
