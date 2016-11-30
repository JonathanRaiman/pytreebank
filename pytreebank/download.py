from __future__ import print_function

import random
import sys
import subprocess

from os import remove, rmdir, stat
from os.path import join, dirname, realpath, exists, isdir, isfile

def execute_bash(command):
    """
    Executes bash command, prints output and throws an exception on failure.

    Arguments:
    ----------
        command : str, bash command to run.

    """
    process = subprocess.Popen(command,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               universal_newlines=True)
    for line in process.stdout:
        print(line, end='', flush=True)
    process.wait()
    assert process.returncode == 0

def delete_paths(paths):
    """
    Delete a list of paths that are files or directories.
    If a file/directory does not exist, skip it.

    Arguments:
    ----------

    paths : list<str>, names of files/directories to remove.

    """
    for path in paths:
        if exists(path):
            if isfile(path):
                remove(path)
            elif isdir(path):
                rmdir(path)

def download_sst(path, url):
    """"
    Download from `url` the zip file corresponding to the
    Stanford Sentiment Treebank and expand the resulting
    files into the directory `path` (Note: if the files are
    already present, the download is not actually run).

    Arguments
    ---------
        path : str, directory to save the train, test, and dev files.
        url : str, location of zip file on the web

    Returns:
    --------

        dict<str, str>: file path for the keys train, test, dev.

    """
    local_files = {
        "train": join(path, "train.txt"),
        "test": join(path, "test.txt"),
        "dev": join(path, "dev.txt")
    }
    if all(exists(fname) and stat(fname).st_size > 100 for fname in local_files.values()):
        return local_files

    zip_local = join(path, 'trainDevTestTrees_PTB.zip')
    delete_paths([zip_local, join(path, "trees")] + local_files.values())
    execute_bash('wget -O %s %s' % (zip_local, url))
    execute_bash('unzip %s -d %s' % (zip_local, path))
    execute_bash('mv %s %s' % (join(path, "trees", "*"), path))
    delete_paths([zip_local, join(path, "trees")])
    return local_files
