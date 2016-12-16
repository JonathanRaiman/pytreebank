# -*- coding: utf-8 -*-
import unittest
import unittest.mock as mock
import tempfile

from shutil import copyfile

from os.path import join, dirname, realpath
from os import makedirs, walk, remove, rmdir

from pytreebank import load_sst
from pytreebank import utils


def add_fake_zip_file(url, path):
    """
    Mock the behavior of urlretrieve by copying over a file
    from a local zip copy.

    Arguments:
    ----------
        url : str, fake origin url
        path : str, destination path for the file to be copied.
    """
    local_zip_file = join(dirname(realpath(__file__)), 'test_download.zip')
    copyfile(local_zip_file, path)


class LoadFakeSST(unittest.TestCase):
    """
    Scaffold and base class for fake
    downloading the Stanford Sentiment Treebank.
    """
    def setUp(self):
        temp_dir = tempfile.gettempdir()
        temp_dir_save_path = join(temp_dir, 'pysst')
        utils.makedirs(temp_dir_save_path, exist_ok=True)
        self.temp_dir_save_path = temp_dir_save_path

    def load_dataset(self):
        """
        Load the dataset into memory.

        Returns:
        --------
            dict: loaded dataset dictionary
        """
        with mock.patch.object(utils, 'urlretrieve') as mock_urlretrieve:
            mock_urlretrieve.side_effect = add_fake_zip_file
            dataset = load_sst(self.temp_dir_save_path)
        return dataset

    def tearDown(self):
        # clean up the fake download
        for root, dirs, files in walk(self.temp_dir_save_path, topdown=False):
            for fname in files:
                remove(join(root, fname))
            for foldername in dirs:
                rmdir(join(root, foldername))


class LoadTests(LoadFakeSST):
    def test_load(self):
        dataset = self.load_dataset()
        for dname in ['train', 'dev', 'test']:
            self.assertTrue(dname in dataset)
            self.assertEqual(len(dataset[dname]), 3)


class LabeledLinesTest(LoadFakeSST):
    def test_loaded_content(self):
        dataset = self.load_dataset()
        # test that the right strings were loaded in:
        self.assertEqual([(3, 'mazaltov')], dataset['train'][-1].to_labeled_lines())
        self.assertEqual([(4, 'tremendous')], dataset['dev'][-1].to_labeled_lines())
        self.assertEqual([(3, 'joyful')], dataset['test'][-1].to_labeled_lines())

        self.assertEqual(['mazaltov'], dataset['train'][-1].to_lines())
        self.assertEqual(['tremendous'], dataset['dev'][-1].to_lines())
        self.assertEqual(['joyful'], dataset['test'][-1].to_lines())

        # test that unfolding trees works correctly
        # and proceeds left to right:
        self.assertEqual(
            [(3, 'hello world'), (2, 'hello'), (2, 'world')],
            dataset['test'][0].to_labeled_lines()
        )
        self.assertEqual(
            [(1, 'bye world'), (2, 'bye'), (2, 'world')],
            dataset['dev'][0].to_labeled_lines()
        )
        self.assertEqual(
            [
                (2, 'hot air balloon'), (1, 'hot air'),
                (2, 'hot'), (2, 'air'), (2, 'balloon')
            ],
            dataset['train'][0].to_labeled_lines()
        )

        self.assertEqual(
            ['hello world', 'hello', 'world'],
            dataset['test'][0].to_lines()
        )
        self.assertEqual(
            ['bye world', 'bye', 'world'],
            dataset['dev'][0].to_lines()
        )
        self.assertEqual(
            ['hot air balloon', 'hot air', 'hot', 'air', 'balloon'],
            dataset['train'][0].to_lines()
        )
