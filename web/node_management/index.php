
<?php
$page_title = "Node Management";
$on_load = "getStatus(); setInterval('getStatus();', 5000);";

require "../common/top.php";
?>

<p>
	<button onclick="requestAction('start all');">Start All Nodes</button>
	<button onclick="requestAction('stop all');">Stop All Nodes</button>
</p>

<div id="status_table_area">Loading...</span>

<?php require "../common/bottom.php"; ?>