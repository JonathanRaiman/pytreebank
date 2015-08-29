function updateTrees() {
	var params = {
		filterByIndexStr: "",
		filterByIndexList: []
	};
	var numTrees = data.trees.length;
	var indexList = [];
	for (var i=0; i<numTrees; i++)
	{
		indexList.push(0);
	}
	params.filterByIndexList = indexList;
	drawTrees( d3.select( "div.trees" ), data.trees, params );
}
// Create global object to visualize trees
var data = {trees: []};

function createTrees(trees) {
	// trees in JSON format.
	data.trees = trees;
}
