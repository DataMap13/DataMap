
<?php
$page_title = "Node Management";
$on_load = "getStatus(); setInterval('getStatus();', 5000);";

require "../common/top.php";
?>

<div id="node_management_content">

	<p>
		<button onclick="requestAction('start all');">Start All Nodes</button>
		<button onclick="requestAction('stop all');">Stop All Nodes</button>
	</p>

	<p>
		<div id="status_table_area">Loading...</div>
	</p>

	<p>
		<button onclick="requestActionSelected('start');">Start Selected Nodes</button>
		<button onclick="requestActionSelected('stop');">Stop Selected Nodes</button>
		<button onclick="requestActionSelected('remove');checkboxes=Array();">Remove Selected Nodes</button>
	</p>
	
</div>

<?php require "../common/bottom.php"; ?>