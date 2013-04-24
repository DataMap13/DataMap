<?php

require("../common/config.php");

$socket = socket_create(AF_INET, SOCK_STREAM, 0);
if (!$socket) {
	die(create_socket_error("Failed to create socket"));
}

if (!socket_connect($socket, $config['server_addr'], $config['control_port'])) {
	die(create_socket_error("Could not connect to socket"));
}

$msg = $_GET['request'];
if (!socket_send($socket, $msg, strlen($msg), 0)) {
	die(create_socket_error("Socket send failed"));
}

if (!socket_recv($socket, $response, 1024, MSG_WAITALL)) {
	die(create_socket_error("Socket receive failed"));
}

?>