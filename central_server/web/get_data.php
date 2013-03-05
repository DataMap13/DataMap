<?php

$connection = mysqli_connect("localhost","datamap13","seniordesign13","network_data");

if (mysqli_connect_errno($connection)) {
	echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$results = mysqli_query($connection,
	"SELECT firstSwitched AS start, lastSwitched AS end, SUM(bytes) AS bytes FROM network_data." . $_GET['table'] . " WHERE NOT ISNULL(bytes) GROUP BY firstSwitched;");

$rows = array();
while($row = mysqli_fetch_array($results)) {
	for ($i = $row['start']; $i <= $row['end']; $i++) {
		$time_span = max($row['end']-$row['start'],1);
		if (!array_key_exists($i,$rows)) {
			$rows[$i]  = array();
			$rows[$i]['time'] = $i;
			$rows[$i]['bytes'] = $row['bytes']*1.0/$time_span;
		} else {
			$rows[$i]['bytes'] += $row['bytes']*1.0/$time_span;
		}
	}
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