<!DOCTYPE html>

<?php
require("config.php");
?>

<html>

	<head>
		<title>DataMap</title>
		<link rel="stylesheet" type="text/css" href="../common/style.css" />
		<script src="//ajax.googleapis.com/ajax/libs/dojo/1.8.3/dojo/dojo.js" data-dojo-config="async:true"></script>
		<script type="text/javascript" src="javascript.js"></script>
	</head>
	
	<body onload="<?php echo $on_load; ?>">
	
		<div id="wrap">
			
			<div id="title">
				DataMap
				<img id="drexel_logo" src="../art/drexel-logo-white.png" />
			</div>
			
			<div id="menu">
				<ul id="menu_list">
					<a href="../node_management/" class="menu_link">
						<li class="menu_item">
							Node Management
						</li>
					</a>
					<a href="../data_analysis/" class="menu_link">
						<li class="menu_item">
							Data Analysis
						</li>
					</a>
				</ul>
			</div>
			
			<div id="page_content">
			
				<h1 id="page_title"><?php echo $page_title; ?></h1>