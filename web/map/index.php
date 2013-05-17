<?php
$page_title = "Map";
$on_load = "load();";

require "../common/top.php";
?>

<script type="text/javascript"
      src="http://maps.googleapis.com/maps/api/js?sensor=false">
    </script>

<div id="map" style="width: 1100px; height: 450px"></div>
<?php require "../common/bottom.php"; ?>
