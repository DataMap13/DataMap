
var updatingGraph = false;

function getTables() {

	require(["dojo/_base/xhr"], function(xhr) {
	
		var select = document.getElementById("tables_select");
		
		while(select.length > 0) select.remove(0);
		select.add(new Option(" -- Select -- ", ""));
		
		xhr.get({
			url: "get_tables.php",
			handleAs: "json",
			load: function(data) {
				for (i in data) {
					var table_name = data[i]['table_name'];
					select.add(new Option(table_name,table_name));
				}
			}
		});
		
		select.disabled = false;
		
	});

}

function getTable() {

	var select = document.getElementById("tables_select");
	return select.options[select.selectedIndex].value;

}

function getGraphs() {

	require([
		"dojo/_base/xhr",
		"dojo/domReady!"
	], function(xhr) {
	
		var select = document.getElementById("graphs_select");
		
		while(select.length > 0) select.remove(0);
		select.add(new Option(" -- Select -- ", ""));
		
		xhr.get({
			url: "get_graphs.php",
			handleAs: "json",
			load: function(data) {
				for (i in data) {
					select.add(new Option(data[i]['name'],data[i]['id']));
				}
			}
		});
		
		select.disabled = false;
		
	});

}

function getGraph() {

	var select = document.getElementById("graphs_select");
	return select.options[select.selectedIndex].value;

}

function updateGraph() {

	if (updatingGraph) return;
	updatingGraph = true;

	if (getTable() == "" || getGraph() == "") {
		document.getElementById("chart_area").innerHTML = "";
		updatingGraph = false;
		return;
	}
	
	require([
		"dojo/_base/xhr",
		"dojo/store/Memory",
		"dojox/charting/Chart",
		"dojox/charting/themes/Dollar",
		"dojox/charting/StoreSeries",
		"dojox/charting/plot2d/StackedAreas",
		"dojox/charting/axis2d/Default",
		"dojo/domReady!"
	], function(xhr,Memory,Chart,theme,StoreSeries) {
	
		xhr.get({
			url: "get_data.php?table=" + getTable() + "&graph=" + getGraph(),
			handleAs: "json",
			load: function(data) {
	
				var store = new Memory({
					data: data,
					idProperty: "time"
				});
				
				document.getElementById("chart_area").innerHTML = "";
				var chart = new Chart("chart_area");
				chart.setTheme(theme);
				
				chart.addPlot("default", {
					type: "StackedAreas"
				});
				
				chart.addAxis("x");
				chart.addAxis("y", { vertical: true });
				
				chart.addSeries("Data1", new StoreSeries(store, {}, "bytes"));
				
				chart.render();
				
				updatingGraph = false;
				
				setTimeout(updateGraph, 1000);
				
			}
		});
	
	});
	

}