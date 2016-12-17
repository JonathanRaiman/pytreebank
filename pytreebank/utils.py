"""
Python 3 / 2 compatibility functions.
"""
import os
import sys

if sys.version_info >= (3,3):
    makedirs = os.makedirs
    def normalize_string(string):
        """
        Standardize input strings by making
        non-ascii spaces be ascii, and by converting
        treebank-style brackets/parenthesis be characters
        once more.

        Arguments:
        ----------
            string : str, characters to be standardized.

        Returns:
        --------
            str : standardized
        """
        return string.replace("\xa0", " ")\
                     .replace("\\", "")\
                     .replace("-LRB-", "(")\
                     .replace("-RRB-", ")")\
                     .replace("-LCB-", "{")\
                     .replace("-RCB-", "}")\
                     .replace("-LSB-", "[")\
                     .replace("-RSB-", "]")
    from urllib.request import urlretrieve
else:
    def makedirs(path, mode=0o777, exist_ok=False):
        if not exist_ok:
            return os.makedirs(path, mode)
        else:
            if not os.path.exists(path):
                return os.makedirs(path, mode)

    def normalize_string(string):
        """
        Standardize input strings by making
        non-ascii spaces be ascii, and by converting
        treebank-style brackets/parenthesis be characters
        once more.

        Arguments:
        ----------
            string : str, characters to be standardized.

        Returns:
        --------
            str : standardized
        """
        return string.replace(u"\xa0", " ")\
                     .replace("\\", "")\
                     .replace("-LRB-", "(")\
                     .replace("-RRB-", ")")\
                     .replace("-LCB-", "{")\
                     .replace("-RCB-", "}")\
                     .replace("-LSB-", "[")\
                     .replace("-RSB-", "]")
    from urllib import urlretrieve

__all__ = ["makedirs", "normalize_string", "urlretrieve"]
