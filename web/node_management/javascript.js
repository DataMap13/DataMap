
function getStatus() {

	var status_table_headers = new Array(
		["ID", "id"],
		["IP Address","ip"],
		["State","state"]
	);

	require(["dojo/_base/xhr"], function(xhr) {
	
		var tableArea = document.getElementById("status_table_area");
		
		xhr.get({
			url: "get_status.php",
			handleAs: "json",
			load: function(data) {
			
				if (data == "") {
					tableArea.innerHTML = "No Known Nodes";
					return;
				}	
			
				var table = document.createElement('table');
				
				header = table.createTHead();
				header_row = header.insertRow(0);
				for (var i = 0; i < status_table_headers.length; i++) {
					var cell = header_row.insertCell(i);
					cell.innerHTML = status_table_headers[i][0];
				}
				var cell = header_row.insertCell(status_table_headers.length);
				cell.innerHTML = "Action";
				
				body = table.createTBody();
				for (var i = 0; i < data.length; i++) {
					var state;
					var row = body.insertRow(i);
					for (var j in status_table_headers) {
						var cell = row.insertCell(j);
						cell.innerHTML = data[i][status_table_headers[j][1]];
						if (status_table_headers[j][1] == "state") {
							state = data[i][status_table_headers[j][1]];
							cell.className = state;
						}
					}
					var cell = row.insertCell(status_table_headers.length);
					var actionSelect = createActionSelect(state);
					cell.appendChild(actionSelect);
				}
			
				tableArea.innerHTML = "";
				tableArea.appendChild(table);
				
			}
		});
	});

}

function createActionSelect(state) {

	var select = document.createElement("select");
	select.add(new Option(" - Action - "));
	
	switch(state) {
		case "DISCONNECTED":
			select.add(new Option("Remove", "Remove"));
			break;
		case "CONNECTED":
			select.add(new Option("Start", "Start"));
			break;
		case "COLLECTING":
			select.add(new Option("Stop", "Stop"));
			break;
		case "ERROR":
			select.add(new Option("Start", "Start"));
			select.add(new Option("Stop", "Stop	"));
			break;
	}
	
	return select;

}