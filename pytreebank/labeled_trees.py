"""
Make trees visualizable in an IPython notebook
"""
import pyximport
pyximport.install()
import json

from IPython.display import Javascript, display

from .javascript import insert_sentiment_markup

try:
    from PIL import ImageFont
    font = ImageFont.core.getfont("/Library/Fonts/Georgia.ttf", 15)
    def text_size(text):
        return max(4, font.getsize(text)[0][0])
except Exception:
    def text_size(text):
        return max(4, int(len(text) * 1.1))
# make changes here to incorporate cap and uncap unknown words.

def dot_product(a, b):
    if type(a) != list:
        a = list(a)
    if type(b) != list:
        b = list(b)
    out = 0.0
    for a_x, b_x in zip(a, b):
        out += a_x * b_x
    return out

class LabeledSentence(object):
    def __init__(self, sentence):
        self.sentence = sentence
        self.label    = None

class LabeledTree(object):

    def __init__(self, depth = 0, sentence = None, label = None, children = None, parent = None, udepth = 1, calculated_embedding = None):
        self.label    = label
        self.predicted_label = None
        self.children = children if children != None else []
        self.general_children = []
        self.sentence = sentence
        self.calculated_embedding = calculated_embedding
        self.parent   = parent
        self.depth    = depth
        self.udepth   = udepth

    def uproot(tree):
        """
        Take a subranch of a tree and deep-copy the children
        of this subbranch into a new LabeledTree
        """
        uprooted = tree.copy()
        uprooted.parent = None
        for child in tree.all_children():
            uprooted.add_general_child(child)
        return uprooted

    def shrink_tree(tree, final_depth):
        if tree.udepth <= final_depth:
            return tree
        for branch in tree.general_children:
            if branch.udepth == final_depth:
                return branch.uproot()

    def shrunk_trees(tree, final_depth):
        if tree.udepth <= final_depth:
            yield tree
        for branch in tree.general_children:
            if branch.udepth == final_depth:
                yield branch.uproot()

    def copy(self):
        """
        Deep Copy of a LabeledTree
        """
        return LabeledTree(
            calculated_embedding = self.calculated_embedding,
            udepth = self.udepth,
            depth = self.depth,
            sentence = self.sentence,
            label = self.label,
            children = self.children.copy() if self.children != None else [],
            parent = self.parent)

    def add_child(self, child):
        """
        Adds a branch to the current tree.
        """
        self.children.append(child)
        child.parent = self
        self.udepth = max([child.udepth for child in self.children]) + 1

    def add_general_child(self, child):
        self.general_children.append(child)

    def all_children(self):
        if len(self.children) > 0:
            for child in self.children:
                for subchild in child.all_children():
                    yield subchild
            yield self
        else:
            yield self

    def lowercase(self):
        """
        Lowercase all strings in this tree.
        Works recursively and in-place.
        """
        if len(self.children) > 0:
            for child in self.children:
                child.lowercase()
        else:
            self.sentence = self.sentence.lower()

    def to_dict(self, index = 1):
        """
        Dict format for use in Javascript / Jason Chuang's display technology.
        """
        rep = {}
        rep["index"] = index
        rep["leaf"] = len(self.children) == 0
        rep["depth"] = self.udepth
        rep["scoreDistr"] = [0.0, 0.0, 0.0, 0.0, 0.0]
        # dirac distribution at correct label
        rep["scoreDistr"][self.label] = 1.0
        rep["scoreDistr"]
        mappping = [-12.5,-6.25,0.0,6.25,12.5]
        rep["rating"] = mappping[self.label] + 12.5
        # if you are using this method for printing predictions
        # from a model, the the dot product with the model's output
        # distribution should be taken with this list:
        # dot_product(predicted_label, mappping) + 12.5
        rep["numChildren"] = len(self.children)
        text = self.sentence if self.sentence != None else ""
        seen_tokens = 0
        witnessed_pixels = 0
        for i, child in enumerate(self.children):
            if i > 0:
                text += " "
            child_key = "child%d" % (i)
            index += 1
            rep[child_key] = child.to_dict(index = index)
            text += rep[child_key]["text"]
            seen_tokens += rep[child_key]["tokens"]
            witnessed_pixels += rep[child_key]["pixels"]

        rep["text"] = text
        rep["tokens"] = 1 if (self.sentence != None and len(self.sentence) > 0) else seen_tokens
        rep["pixels"] = witnessed_pixels + 3 if len(self.children) > 0 else text_size(self.sentence)
        return rep

    def to_json(self):
        return json.dumps(self.to_dict())

    def display(self):
        display(Javascript("createTrees(["+self.to_json()+"])"))
        display(Javascript("updateTrees()"))

    def to_lines(self):
        if len(self.children) > 0:
            left_lines, right_lines = self.children[0].to_lines(), self.children[1].to_lines()
            self_line = [left_lines[0] + " " + right_lines[0]]
            return self_line + left_lines + right_lines
        else:
            return [self.sentence]

    def to_labeled_lines(self):
        if len(self.children) > 0:
            left_lines, right_lines = self.children[0].to_labeled_lines(), self.children[1].to_labeled_lines()
            self_line = [(self.label, left_lines[0][1] + " " + right_lines[0][1])]
            return self_line + left_lines + right_lines
        else:
            return [(self.label, self.sentence)]

    def __str__(self):
        """
        String representation of a tree as visible in original corpus.

        print(tree)
        #=> '(2 (2 not) (3 good))'

        Outputs
        -------

            str: the String representation of the tree.

        """
        if len(self.children) > 0:
            rep = "(%d " % self.label
            for child in self.children:
                rep += str(child)
            return rep + ")"
        else:
            text = self.sentence\
                .replace("(", "-LRB-")\
                .replace(")", "-RRB-")\
                .replace("{", "-LCB-")\
                .replace("}", "-RCB-")\
                .replace("[", "-LSB-")\
                .replace("]", "-RSB-")

            return ("(%d %s) " % (self.label, text))

    @staticmethod
    def inject_visualization_javascript():
        """
        In an Ipython notebook, show SST trees using the same Javascript
        code as used by Jason Chuang's visualisations.
        """
        insert_sentiment_markup()
