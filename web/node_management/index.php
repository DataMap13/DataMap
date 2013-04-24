
<?php
$page_title = "Node Management";
$on_load = "getStatus(); setInterval('getStatus();', 5000);";

require "../common/top.php";
?>

<div id="status_table_area">Loading...</span>

<?php require "../common/bottom.php"; ?>