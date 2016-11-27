from os.path import realpath, dirname, join
from IPython.display import HTML, display

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
	import_tag(
		"script",
		contents=format_replacements(open(scriptname).read(), replacements),
		type="text/javascript"
	)

def import_css(cssname):
	import_tag("style", contents=open(cssname).read())

def insert_stanford_javascript(tree_width=1200, tree_height=400, tree_node_radius=10):
	import_javascript(join(SCRIPT_DIR, "c3.min.js"))
	import_javascript(join(SCRIPT_DIR, "d3.min.js"))
	import_javascript(join(SCRIPT_DIR, "sentree.min.js"))
	import_javascript(join(SCRIPT_DIR, "sentrees.min.js"),
		{
			"treeWidth":tree_width,
			"treeHeight":tree_height,
			"treeNodeRadius":tree_node_radius
		})
	import_javascript(join(SCRIPT_DIR, "tree_visualization.js"))

def insert_stanford_styles():
	import_css(join(SCRIPT_DIR, "tree_visualization.css"))

def insert_sentiment_markup(tree_width=1200, tree_height=400, tree_node_radius=10):
	insert_stanford_javascript(
		tree_width=tree_width,
		tree_height=tree_height,
		tree_node_radius=tree_node_radius
	)
	insert_stanford_styles()
	import_tag("div", className='trees')
