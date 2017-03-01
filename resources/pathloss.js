'use strict'

var map = undefined;
var txMarker = undefined;
var rxMarker = undefined;

$(document).ready(function() {    	 
	$("#loader").hide();
	
	$("#txlat").keyup(function(){
	    update();
	});
	$("#txlng").keyup(function(){
	    update();
	});
	$("#rxlat").keyup(function(){
	    update();
	});
	$("#rxlng").keyup(function(){
	    update();
	});
	
	// Page has loaded now see if we have data in the URL
/*	if (/txLng/.test(window.location.href)) {
		profileOnPageLoad();
	}
*/	
	$("#btnSubmit").click(function(){
/*		var txLat = $("#txlat").val();
		var txLng = $("#txlng").val();
		var rxLat = $("#rxlat").val();
		var rxLng = $("#rxlng").val();
*/
/*		
		Cookies.set('txlatProfile', txLat, { expires: 3650, path: '' });
		Cookies.set('txlngProfile', txLng, { expires: 3650, path: '' });
		Cookies.set('rxlatProfile', rxLat, { expires: 3650, path: '' });
		Cookies.set('rxlngProfile', rxLng, { expires: 3650, path: '' }); 
*/
		
		var getData = "?frequency=18" + "&distance=26.083" + "&txAntennaDiameter=1.8" + "&rxAntennaDiameter=0.8" + 
		"&txAntennaGain=48.0109" + "&rxAntennaGain=40.96725" + "&txPower=15" + "&rxSensetivity=-100" + 
		"&txConnectorLosses=0" + "&rxConnectorLosses=0" + "&txCableLosses=0" + "&rxCableLosses=0";

		//console.log(getData);
/*		18 26.083 1.8 0.8 48.0109 40.96725 15 -100 0 0 0 0   */
		/*/cgi-bin/pathloss.py*/
	    $.ajax({
		    url: "/cgi-bin/pathloss.py" + getData,
		    type: "GET",
		    beforeSend: function(){
                $("#loader").show();
            },
		    success: function(response){
   			    history.pushState({}, null, "http://www.predtest.uk/pathloss/pathloss.html" + getData)

                $("#loader").hide();
                console.log(response);
			    if ( (response != null) ) {
                	//createProfile(response);
                	  document.getElementById('fresnelRadius').innerText = response.linkCalculations.fresnelRadius;
                	  document.getElementById('farFieldStart').innerText = response.linkCalculations.farFieldStart;
                	  document.getElementById('fadeMargin').innerText = response.linkCalculations.fadeMargin;
                	  document.getElementById('linkAvailability').innerText = response.linkCalculations.linkAvailability;
			    } else {
				    alert("Error: I'm sorry there was a problem generating the pathloss");
			    }
		    },
            error: function (error) {
	            console.log(error);
                $("#loader").hide();
			    alert("Error: I'm sorry there was a problem generating the pathloss");
            }	
		});
	});

	function createPathloss(data) {		
		var x = [];
		var y = [];
		var z = [];
		
		var len = data.points.length;
		var startHeight = data.points[0].trueheight - data.points[0].curheight;
		var endHeight = data.points[len-1].trueheight - data.points[len-1].curheight;
		var difference = 0;
		var move = startHeight;
	
		difference = startHeight - endHeight;
		// if difference is positive, start is higher, if 
		// difference is negative, start is lower
		
		var slopeDiff = difference / len;
		
		var title = 'Point To Point Pathloss (' + data.points[0].ycoord + ' ' + data.points[0].xcoord + ' to ' + data.points[len-1].ycoord + ' ' + data.points[len-1].xcoord + ')';
		for (var i = 0; i < len; i++) {
			x.push(i);
			y.push(data.points[i].trueheight - data.points[i].curheight);
			z.push(move);
			if (difference < 0) { // need to add our difference
				move += -slopeDiff
			} else {
				move -= slopeDiff
			}
		}
		
		var trace = {
			x: x, 
			y: y, 
	  		type: 'scatter',
	  		mode: 'lines',
	  		line: {shape: 'spline'},
	  		fill: 'tozeroy'
		};
		var slope = {
			x: x, 
			y: z,
	  		type: 'scatter',
	  		mode: 'lines',
	  		line: {shape: 'spline'}
	  	};
		
		
		var layout = {
			title: title,
			showlegend: false,
			xaxis: {
				title: '<-- Distance: ' + data.output.dist + 'km -->',
			    showticklabels: false
	  		},
	  		yaxis: {
	  			title: 'Height (m)'
	  		}
		};
		
		var plotData = [trace, slope];
		Plotly.newPlot('profileDiv', plotData, layout);	
	}
});

function getURLParameter(name) {
  return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search) || [null, ''])[1].replace(/\+/g, '%20')) || null;
}
