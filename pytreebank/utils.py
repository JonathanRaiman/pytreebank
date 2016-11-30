"""
Python 3 / 2 compatibility functions.
"""
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
else:
    def makedirs(path, mode=0o777, exist_ok=False):
        if not exist_ok:
            return makedirs(path, mode)
        else:
            if not os.path.exists(path):
                return makedirs(path, mode)

    def normalize_string(string):
        return string.replace(u"\xa0", " ")\
                     .replace("\\", "")\
                     .replace("-LRB-", "(")\
                     .replace("-RRB-", ")")\
                     .replace("-LCB-", "{")\
                     .replace("-RCB-", "}")\
                     .replace("-LSB-", "[")\
                     .replace("-RSB-", "]")

__all__ = ["makedirs", "normalize_string"]
