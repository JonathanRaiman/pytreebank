"""
Make trees visualizable in an IPython notebook
"""
import pyximport
pyximport.install()
import json

try:
    from PIL import ImageFont
    from IPython.display import Javascript, display
    font = ImageFont.core.getfont("/Library/Fonts/Georgia.ttf", 15)
    def text_size(text):
        return max(4, font.getsize(text)[0][0])
except Exception:
    def text_size(text):
        return max(4, int(len(s) * 1.1))
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
        return LabeledTree(
            calculated_embedding = self.calculated_embedding,
            udepth = self.udepth,
            depth = self.depth,
            sentence = self.sentence,
            label = self.label,
            children = self.children.copy() if self.children != None else [],
            parent = self.parent)

    def add_child(self, child):
        self.children.append(child)
        # assert(child.depth == self.depth + 1)
        child.parent = self

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
        if len(self.children) > 0:
            for child in self.children:
                child.lowercase()
        else:
            self.sentence = self.sentence.lower()

    def true_label(self, model):
        return model.true_label(self)

    def to_dict(self, model, index = 1, prediction = True):
        """
        Dict format for use in Javascript / Jason Chuang's display technology.
        """
        rep = {}
        rep["index"] = index
        rep["leaf"] = len(self.children) == 0
        rep["depth"] = self.udepth
        if prediction:
            pred_label = self.predicted_label
        else:
            pred_label = self.true_label(model)
        rep["scoreDistr"] = pred_label.tolist()
        rep["rating"] = dot_product(pred_label, [-12.5,-6.25,0.0,6.25,12.5])+12.5
        rep["numChildren"] = len(self.children)
        text = self.sentence if self.sentence != None else ""
        seen_tokens = 0
        witnessed_pixels = 0
        for i, child in enumerate(self.children):
            if i > 0:
                text += " "
            child_key = "child%d" % (i)
            index += 1
            rep[child_key] = child.to_dict(model, index = index, prediction = prediction)
            text += rep[child_key]["text"]
            seen_tokens += rep[child_key]["tokens"]
            witnessed_pixels += rep[child_key]["pixels"]

        rep["text"] = text
        rep["tokens"] = 1 if (self.sentence != None and len(self.sentence) > 0) else seen_tokens
        rep["pixels"] = witnessed_pixels + 3 if len(self.children) > 0 else text_size(self.sentence)
        return rep

    def to_json(self, model, prediction = True):
        return json.dumps(self.to_dict(model, prediction = prediction))

    def display(tree, model, prediction = True):
        if prediction:
            model.forward_propagate(tree)
        display(Javascript("createTrees(["+tree.to_json(model, prediction = prediction)+"])"))
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


    def total_projections_predictions(self, model = None):
        return total_projections_predictions(self, model)

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
            return ("(%d %s) " % (self.label, self.sentence))
