from IPython.display import Javascript, HTML, display

from os.path import realpath, dirname, join

SCRIPT_DIR = dirname(realpath(__file__))


def import_tag(tagname, contents = "", **kwargs):
	html = "<%s " % (tagname)
	for key, val in kwargs.items():
		if key == 'className':
			key = 'class' # to avoid Python issues
		html += "%s='%s' " % (key, val)
	html += ">"
	html += contents
	html += "</%s>" % (tagname)
	display(HTML(html))

def format_replacements(content, replacements):
	for key, value in replacements.items():
		content = content.replace("{" + key + "}", str(value))
	return content

def import_javascript(scriptname, replacements=None):
	if replacements is None:
		replacements = {}
	import_tag("script", contents = format_replacements(open(scriptname).read(), replacements), type = "text/javascript")

def import_css(cssname):
	import_tag("style", contents = open(cssname).read())

def insert_stanford_javascript(treeWidth=1200, treeHeight=400, treeNodeRadius=10):
	import_javascript(join(SCRIPT_DIR, "c3.min.js"))
	import_javascript(join(SCRIPT_DIR, "d3.min.js"))
	import_javascript(join(SCRIPT_DIR, "sentree.min.js"))
	import_javascript(join(SCRIPT_DIR, "sentrees.min.js"),
		{
			"treeWidth":treeWidth,
			"treeHeight":treeHeight,
			"treeNodeRadius":treeNodeRadius
		})
	import_javascript(join(SCRIPT_DIR, "tree_visualization.js"))

def insert_stanford_styles():
	import_css(join(SCRIPT_DIR, "tree_visualization.css"))

def insert_sentiment_markup(treeWidth=1200, treeHeight=400, treeNodeRadius=10):
	insert_stanford_javascript(treeWidth=treeWidth, treeHeight=treeHeight, treeNodeRadius=treeNodeRadius)
	insert_stanford_styles()
	import_tag("div", className='trees')
