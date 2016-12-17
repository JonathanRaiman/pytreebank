from os import remove, rmdir, stat
from os.path import join, dirname, realpath, exists, isdir, isfile

from zipfile import ZipFile
from shutil import move
from . import utils


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
    delete_paths([zip_local, join(path, "trees")] + list(local_files.values()))
    utils.urlretrieve(url, zip_local)
    ZipFile(zip_local).extractall(path)
    for fname in local_files.values():
        move(join(path, 'trainDevTestTrees_PTB', 'trees', fname.split('/')[-1]), fname)
    delete_paths([zip_local, join(path, 'trainDevTestTrees_PTB', 'trees'), join(path, 'trainDevTestTrees_PTB')])
    return local_files
