function SVGTree(divName)
{
    // Div which the tree is rendered in
    this._divName = divName;

    // Canvas parameters
    this._canvasW = 800;
    this._canvasH = 600;

    // Viewbox parameters
    this._vbX = 0;
    this._vbY = 0;
};

SVGTree.prototype.div = function(divName)
{
    if (arguments.length != 0)
	this._divName = divName;
    else
	return this._divName;
};

SVGTree.prototype.moveView = function(dx, dy)
{
    var newX = this._vbX + dx;
    var newY = this._vbY + dy;
    var update = false;

    var thisAlias = this;

    if ( (newX > 0) && (newX < this._canvasW))
    {
	this._vbX = newX;
	update = true;
    }

    if ( (newY > 0) && (newY < this._canvasH))
    {
	this._vbY = newY;
	update = true;
    }

    if (update)
	d3.select("#canvas").attr("viewBox", ""+ thisAlias._vbX + " " + thisAlias._vbY + " " + thisAlias._canvasW + " " + this._canvasH);
};

SVGTree.prototype.projFunc = function(scale, pos)
{
    return (1 + (0.01 * scale))*pos + 20;
};

SVGTree.prototype.radiusFunc = function(text)
{
    return 10*Math.sqrt(text.length);
};

SVGTree.prototype.dispTree = function(treeData)
{
    d3.selectAll("svg").remove();
    this._vbX = 0;
    this._vbY = 0;

    var thisAlias = this;

    var vis = d3.select("#"+this._divName).append("svg:svg")
	.attr("width", this._canvasW)
	.attr("height", this._canvasH)
        .attr("id", "canvas")
	.append("svg:g")
	.attr("transform", "translate(40, 10)")
        .attr("viewbox", ""+ thisAlias._vbX + " " + thisAlias._vbY + " " + thisAlias._canvasW + " " + thisAlias._canvasH);

    var nnum = treeData.numNodes();
    

    var tree = d3.layout.tree()
	.size([thisAlias._canvasW-100,thisAlias._canvasH-100]);

    var diagonal = d3.svg.diagonal()
	.projection(function(d) { return [thisAlias.projFunc(nnum, d.x), thisAlias.projFunc(nnum, d.y)]; });

    var nodes = tree.nodes(treeData.toViz());

    var link = vis.selectAll("pathlink")
	.data(tree.links(nodes))
	.enter().append("svg:path")
	.attr("class", "link")
	.attr("d", diagonal);

    var node = vis.selectAll("g.node")
	.data(nodes)
	.enter().append("svg:g")
	.attr("transform", function(d) { return "translate(" + thisAlias.projFunc(nnum, d.x) + "," + thisAlias.projFunc(nnum, d.y) + ")"; })

    node.append("svg:circle")
	.attr("r", function(d) { return thisAlias.radiusFunc(d.dispText); })
        .attr("class", function(d) { return d.type == "text" ? "leaf" : ""; });

    node.append("svg:text")
	.attr("dy", ".3em")
	.attr("text-anchor", "middle")
	.text(function(d) { return d.dispText; });
};

SVGTree.prototype.updateNode = function(updateFunc)
{
    // Alias to this for use within d3 functions
    var thisAlias = this;

    var node = d3.select("#"+this._divName);

    // Should this be a deep copy of d to make sure you can't modify d?
    var data = node.selectAll("text").data();
    for(var i = 0; i < data.length; i++)
    {
	data[i].dispText = updateFunc(data[i]);
    }
    node.data(data);

    // Update the text that will be displayed
    // and the radius of the node based on the newly
    // displayed text
    node.selectAll("text").text(function(d) { return d.dispText; });
    node.selectAll("circle").attr("r", function(d) { return thisAlias.radiusFunc(d.dispText); });
};

SVGTree.prototype.nodeClass = function(updateClass)
{
    var node = d3.select("#"+this._divName);

    if(arguments.length != 0)
    {
	node.selectAll("circle").attr("class", function(d) { return updateClass(d); });
    }
};
