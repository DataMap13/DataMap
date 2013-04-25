
<?php
$page_title = "Node Management";
$on_load = "getStatus(); setInterval('getStatus();', 5000);";

require "../common/top.php";
?>

<p>
	<button onclick="requestAction('start all');">Start All Nodes</button>
	<button onclick="requestAction('stop all');">Stop All Nodes</button>
</p>

<p>
	<div id="status_table_area">Loading...</div>
</p>

<p>
	<button onclick="requestActionSelected('start')">Start Selected Nodes</button>
	<button onclick="requestActionSelected('stop')">Stop Selected Nodes</button>
	<button onclick="requestActionSelected('remove')">Remove Selected Nodes</button>
</p>

<?php require "../common/bottom.php"; ?>