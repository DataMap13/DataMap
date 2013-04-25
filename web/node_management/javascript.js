
var checkboxes = Array();

var h_checkbox = document.createElement("input");
h_checkbox.type = "checkbox";
h_checkbox.onchange = function() {
	for (var i = 0; i < checkboxes.length; i++)
		checkboxes[i].checked = h_checkbox.checked;
};

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
				
				header_row.insertCell(header_row.cells.length).appendChild(h_checkbox);
				
				header_row.insertCell(header_row.cells.length).innerHTML = "ID";
				header_row.insertCell(header_row.cells.length).innerHTML = "IP Address";
				header_row.insertCell(header_row.cells.length).innerHTML = "State";
				header_row.insertCell(header_row.cells.length).innerHTML = "Action";
				
				body = table.createTBody();
				for (var i = 0; i < data.length; i++) {
				
					var row = body.insertRow(i);
					
					var checkbox_cell = row.insertCell(row.cells.length);
					if (checkboxes[i] == null) {
						checkboxes[i] = document.createElement("input");
						checkboxes[i].type = "checkbox";
					}
					checkboxes[i].value = data[i]['ip']
					checkbox_cell.appendChild(checkboxes[i]);
					
					row.insertCell(row.cells.length).innerHTML = data[i]['id'];
					row.insertCell(row.cells.length).innerHTML = data[i]['ip'];
					
					var state_cell = row.insertCell(row.cells.length)
					state_cell.innerHTML = data[i]['state'];
					if (data[i]['state'].match('ERROR'))
						data[i]['state'] = "ERROR";
					state_cell.className = data[i]['state'];
					
					var action_cell = row.insertCell(row.cells.length)
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

	alert("Requesting: " + request);

	require(["dojo/_base/xhr"], function(xhr) {
	
		xhr.get({
			url: "request_action.php?request=" + encodeURI(request)
		});
		
	});

}

function requestActionSelected(action) {

	var request = action + " ";
	
	for (var i = 0; i < checkboxes.length; i++)
		if (checkboxes[i].checked)
			request += checkboxes[i].value + " ";
			
	requestAction(request);

}