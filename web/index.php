<!DOCTYPE html>

<html>

	<head>
		<title>DataMap</title>
		<script src="//ajax.googleapis.com/ajax/libs/dojo/1.8.3/dojo/dojo.js" data-dojo-config="async:true"></script>
		<script type="text/javascript" src="index.js"></script>
	</head>
	
	<body onload="getTables();getGraphs();">
	
		<h1 id="greeting">DataMap</h1>
		
		Table:
		<select disabled id="tables_select" onchange="updateGraph();">
			<option selected>Loading...</option>
		</select>
		
		Graph:
		<select disabled id="graphs_select" onchange="updateGraph();">
			<option>Loading...</option>
		</select>
		
		<div id="chart_area"></div>
	
	</body>
	
</html>