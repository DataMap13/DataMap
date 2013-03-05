<?php

$connection = mysqli_connect("localhost","datamap13","seniordesign13","network_data");

if (mysqli_connect_errno($connection)) {
	echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$results = mysqli_query($connection,
	"SELECT TABLE_NAME AS table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'network_data' AND table_name != 'exporter';");

$rows = array();
while($row = mysqli_fetch_array($results)) {
	$rows[] = $row;
}

print json_encode($rows);

mysqli_close($connection); 

?>