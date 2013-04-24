
function getStatus() {

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
				var header_row = header.insertRow(0);
				header_row.insertCell(0).innerHTML = "ID";
				header_row.insertCell(1).innerHTML = "IP Address";
				header_row.insertCell(2).innerHTML = "State";
				header_row.insertCell(3).innerHTML = "Action";
				
				body = table.createTBody();
				for (var i = 0; i < data.length; i++) {
				
					var row = body.insertRow(i);
					
					row.insertCell(0).innerHTML = data[i]['id'];
					row.insertCell(1).innerHTML = data[i]['ip'];
					
					var state_cell = row.insertCell(2)
					state_cell.innerHTML = data[i]['state'];
					if (data[i]['state'].match('ERROR'))
						data[i]['state'] = "ERROR";
					state_cell.className = data[i]['state'];
					
					var action_cell = row.insertCell(3)
					action_cell.appendChild(createActionSelect(data[i]['state'],data[i]['ip']));
					
				}
			
				tableArea.innerHTML = "";
				tableArea.appendChild(table);
				
			}
		});
	});

}

function createActionSelect(state,ip) {

	var select = document.createElement("select");
	select.add(new Option(" - Action - "));
	
	select.onchange = function() {
		requestAction(select.options[select.selectedIndex].value + " " + ip);
	};
	
	switch(state) {
		case "DISCONNECTED":
			select.add(new Option("Remove", "remove"));
			break;
		case "CONNECTED":
			select.add(new Option("Start", "start"));
			break;
		case "COLLECTING":
			select.add(new Option("Stop", "stop"));
			break;
		case "ERROR":
			select.add(new Option("Start", "start"));
			select.add(new Option("Stop", "stop	"));
			break;
	}
	
	return select;

}

function requestAction(request) {

	require(["dojo/_base/xhr"], function(xhr) {
	
		xhr.get({
			url: "request_action.php?request=" + encodeURI(request)
		});
		
	});

}