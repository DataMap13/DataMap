
<?php
$page_title = "Data Analysis";
$on_load = "getTables();getGraphs();";

require "../common/top.php";
?>

Table:
<select disabled id="tables_select" onchange="updateGraph();">
	<option selected>Loading...</option>
</select>

Graph:
<select disabled id="graphs_select" onchange="updateGraph();">
	<option>Loading...</option>
</select>

<div id="chart_area"></div>

<?php require "../common/bottom.php"; ?>