from collections import OrderedDict

class LabeledTreeCorpus(list):
    """
    Read in the Stanford Sentiment Treebank using the original serialization format:

    > (3 (2 this) (3 (2 is) (3 good ) )

    """

    def labels(self):
        labelings = OrderedDict()
        for tree in self:
            for label, line in tree.to_labeled_lines():
                labelings[line] = label
        return labelings

    def to_file(self, path, mode = "w"):
        with open(path, mode = mode) as f:
            for tree in self:
                for label, line in tree.to_labeled_lines():
                    f.write(line + "\n")
