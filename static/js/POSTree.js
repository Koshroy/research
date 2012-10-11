function POSTree(tree)
{
    this._tree = tree;
};

POSTree.prototype.tree = function(newTree)
{
    if (arguments.length != 0)
 	this._tree = newTree;
     else
	return this._tree;
}

POSTree.prototype.numNodes = function()
{
    var stack = new Array();
    var cnt = 0;
    stack.push(this._tree);

    while(stack.length != 0)
    {
	var node = stack.pop();
	cnt++;
	if (node.type == "pos")
	{
	    for(var i = 0; i < node.args.length; i++)
	    {
		stack.push(node.args[i]);
	    }
	}
    }

    return cnt;
};

POSTree.prototype.toViz = function()
{
    var newPosTree = $.extend(true, {}, this._tree);

    var stack = new Array();
    stack.push(newPosTree);
    while(stack.length != 0)
    {
	var node = stack.pop();
	node.name = node.pos;

	if (node.type == "pos")
	{
	    node.children = node.args;
	    for(var i = 0; i < node.children.length; i++)
	    {
		stack.push(node.children[i]);
	    }
	    node.dispText = node.pos;
	}

	else if (node.type == "text")
	{
	    node.text = node.args[0];
	    node.dispText = node.text;
	}

	else if (node.type == "dot")
	{
	    node.dispText = ".";
	}
	delete node.args;
	//delete node.type;
    }

    return newPosTree;
};


