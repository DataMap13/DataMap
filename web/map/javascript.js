

    function load() {
      var map = new google.maps.Map(document.getElementById("map"), {
        center: new google.maps.LatLng(39.954746, -75.185677),
        zoom: 15,
        mapTypeId: 'roadmap'
      });
      var infoWindow = new google.maps.InfoWindow;

      require(["dojo/_base/xhr"], function(xhr) {
      // Change this depending on the name of your PHP file
	      xhr.get({
				url: "../node_management/get_status.php",
				handleAs: "json",
				load: function(data) {
					for (var i = 0; i < data.length; i++) {
					  var id = data[i]['id'];
					  var address = data[i]['ip'];
					  var point = new google.maps.LatLng(
						  parseFloat(data[i]['lat']),
						  parseFloat(data[i]['long']));
					  var html = "<b>" + id + "</b> <br/>" + address;
					  var icon = 'http://labs.google.com/ridefinder/images/mm_20_red.png';
            var shadow = 'http://labs.google.com/ridefinder/images/mm_20_shadow.png';
					  var marker = new google.maps.Marker({
						map: map,
						position: point,
						icon: icon,
						shadow: shadow
					  });
					  bindInfoWindow(marker, map, infoWindow, html);
					}	
				}
	      });
	    });
    }

    function bindInfoWindow(marker, map, infoWindow, html) {
      google.maps.event.addListener(marker, 'click', function() {
        infoWindow.setContent(html);
        infoWindow.open(map, marker);
      });
    }

    // function downloadUrl(url, callback) {
    //   var request = window.ActiveXObject ?
    //       new ActiveXObject('Microsoft.XMLHTTP') :
    //       new XMLHttpRequest;

    //   request.onreadystatechange = function() {
    //     if (request.readyState == 4) {
    //       request.onreadystatechange = doNothing;
    //       callback(request, request.status);
    //     }
    //   };

    //   request.open('GET', url, true);
    //   request.send(null);
    // }

    function doNothing() {}

    //]]>