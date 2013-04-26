<?php

require("../common/config.php");

$connection = mysqli_connect($config['server_addr'], $config['db_username'], $config['db_password'], $config['db_name']);
if (mysqli_connect_errno($connection)) {
	die("Failed to connect to MySQL: " . mysqli_connect_error());
}

$results = mysqli_query($connection,
	"SELECT firstSwitchedMillis AS time, SUM(bytes) AS bytes FROM network_data." . $_GET['table'] . " WHERE NOT ISNULL(bytes) GROUP BY firstSwitchedMillis;");
if (!$results) {
	die("Error executing mysql query: " . mysqli_error($connection));
}

$rows = array();
while($row = mysqli_fetch_array($results)) {
	$rows[] = $row;
}

$rows2 = array();
$count = 0;
foreach ($rows as $row) {
	if ($count >= 39) break;
	$rows2[] = $row;
	$count++;
}

print json_encode($rows2);
	
?>