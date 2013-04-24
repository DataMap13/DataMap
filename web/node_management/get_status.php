<?php

require("../common/config.php");

$socket = socket_create(AF_INET, SOCK_STREAM, 0);
if (!$socket) {
	die(create_socket_error("Failed to create socket"));
}

// TODO: Make this configurable
if (!socket_connect($socket, $config['server_addr'], $config['control_port'])) {
	die(create_socket_error("Could not connect to socket"));
}

$msg = "status";
if (!socket_send($socket, $msg, strlen($msg), 0)) {
	die(create_socket_error("Socket send failed"));
}

if (!socket_recv($socket, $response, 1024, MSG_WAITALL)) {
	die(create_socket_error("Socket receive failed"));
}

$nodes = array();
foreach (preg_split("/\n/",$response) as $line) {
	if ($line == "") continue;
	$vals = preg_split("/\|/", $line);
	$nodes[] = array(
		"ip" => $vals[0],
		"id" => $vals[1],
		"state" => $vals[2]
	);
}

print json_encode($nodes);

function create_socket_error($msg) {
	$error_code = socket_last_error();
	$error_string = socket_strerror($error_code);
	return $msg . "[" . $error_code . "]: " . $error_string;
}

?>