"""
Special loading methods for importing dataset as processed
by the TreeLSTM code from https://github.com/stanfordnlp/treelstm
"""
from .labeled_trees       import LabeledTree
import codes

def import_tree_corpus(labels_path, parents_path, sentences_path):
    """
    Import dataset from the TreeLSTM data generation scrips.

    Inputs
    ------

    labels_path: where are labels are stored (should be in data/sst/labels.txt)
    parents_path: where the parent relationships are stored (should be in data/sst/parents.txt)
    sentences_path: where are strings for each tree are stored (should be in data/sst/sents.txt)

    Outputs
    -------

    trees : a list of LabeledTree
    """
    with codecs.open(labels_path, "r", "UTF-8") as f:
        label_lines = f.readlines()
    with codecs.open(parents_path, "r", "UTF-8") as f:
        parent_lines = f.readlines()
    with codecs.open(sentences_path, "r", "UTF-8") as f:
        word_lines = f.readlines()
    assert len(label_lines) == len(parent_lines)
    assert len(label_lines) == len(word_lines)

    trees = []

    for labels, parents, words in zip(label_lines, parent_lines, word_lines):
        labels  = [int(l) + 2 for l in labels.strip().split(" ")]
        parents = [int(l) for l in parents.strip().split(" ")]
        words   = words.strip().split(" ")
        assert len(labels) == len(parents)
        trees.append(read_tree(parents, labels, words))
    return trees

def assign_sentences(node, words, next_idx=0):
    """
    Recursively assign the words to nodes by finding and
    assigning strings to the leaves of a tree in left
    to right order.
    """
    if len(node.children) == 0:
        node.sentence = words[next_idx]
        return next_idx + 1
    else:
        for child in node.children:
            next_idx = assign_sentences(child, words, next_idx)
        return next_idx

def read_tree(parents, labels, words):
    """
    Take as input a list of integers for parents
    and labels, along with a list of words, and
    reconstruct a LabeledTree.
    """
    trees = {}
    root = None
    for i in range(1, len(parents) + 1):
        if not i in trees and parents[i - 1] != - 1:
            idx = i
            prev = None
            while True:
                parent = parents[idx - 1]
                if parent == -1:
                    break
                tree = LabeledTree()
                if prev is not None:
                    tree.add_child(prev)
                trees[idx] = tree
                tree.label = labels[idx - 1]
                if trees.get(parent) is not None:
                    trees[parent].add_child(tree)
                    break
                elif parent == 0:
                    root = tree
                    break
                else:
                    prev = tree
                    idx = parent
    assert assign_sentences(root, words) == len(words)
    return root
