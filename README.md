SST Utils
---------

Utilities for loading and visualizing Stanford Sentiment Treebank.
See examples below for usage.

@author Jonathan Raiman

Javascript code by Jason Chuang and Stanford NLP modified and taken from [Stanford NLP Sentiment Analysis demo](http://nlp.stanford.edu:8080/sentiment/rntnDemo.html).

### Visualization

Allows for visualization using Jason Chuang's Javascript and CSS within an IPython notebook:

```python
import pytreebank
# load the sentiment treebank corpus in the parenthesis format,
# e.g. "(4 (2 very ) (3 good))"
dataset = pytreebank.import_tree_corpus("train.txt")
# add Javascript and CSS to the Ipython notebook
pytreebank.LabeledTree.inject_visualization_javascript()
# select and example to visualize
example = dataset[0]
# display it in the page
example.display()
```

![Example visualization using pytreebank](visualization_example.png)

### Lines and Labels

To use the corpus to output spans from the different trees you can call the `to_labeled_lines` and `to_lines` method of a `LabeledTree`. The first returned sentence in those lists is always the root sentence:

```python
import pytreebank
dataset = pytreebank.import_tree_corpus("train.txt")
example = dataset[0]

# extract spans from the tree.
for label, sentence in example.to_labeled_lines():
	print("%s has sentiment label %s" % (
		sentence,
		["very negative", "negative", "neutral", "positive", "very positive"][label]
	))
```


