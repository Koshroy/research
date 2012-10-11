var sTree;

function readyFunc()
{
    sTree = new SVGTree("viz");
    
    $("#parseForm").submit(function() {
	var sent = $("#sentenceText").val();
	console.log(sent);
	if (sent != "")
	    $.post("/sentparse",
		   { "sentence" : sent},
		   function(a) { 
		       var relations = $("#relSelect").val();
		       sTree.dispTree(new POSTree(a));
		       sTree.nodeClass(function(d) {
			   console.log("Uguu: " + relations.indexOf(d.dispText));
			   if (relations.indexOf(d.dispText) > -1)  return  "relation";  });
		   },
		   "json");
	return false;
    });

    $("#addRelBut").click(function () {
	var relText = $("#relText").val();
	console.log(relText);

	if (relText != "")
	    $("#relSelect").append(new Option(relText, relText, true, true));
	return false;
    });

    $(document).keydown(function(event){
	console.log("keydown");

	var vbX=0, vbY=0;

	switch(event.which)
	{
	case 37: // Left
	    vbX -= 10;
	    event.preventDefault();
	    break;
	case 38: // Up
	    vbY -= 10;
	    break;
	case 39: // Right
	    vbX += 10;
	    break;
	case 40: // Down
	    vbY += 10;
	    event.preventDefault();
	    break;
	}
	//d3.select("#canvas").attr("viewBox", ""+ vbX + " " + vbY + " " + canvasW + " " + canvasH);
	sTree.moveView(vbX, vbY);
	return true;
    });

    $("#showLeafCheck").live('change', function(){ 
	if ($(this).attr('checked') != "checked")
	{
	    sTree.updateNode(function(d) { return d.type == "text" ? d.text : d.pos; });
	}
	else
	{
	    sTree.updateNode(function(d) { return d.pos; });
	}
    });
}

$(document).ready(readyFunc);