'use strict'

var map = undefined;
var txMarker = undefined;
var rxMarker = undefined;
var units = 'db';

$(document).ready(function() {    	 
	$("#loader").hide();
		
	$("#frequency").val(18);
	$("#distance").val(26.083);

	$("#txConnector").val(0);
	$("#txCable").val(0);
	$("#txDiameter").val(1.8);
	$("#txGain").val(48.0109);
	$("#txPower").val(15);
	
	
	$("#rxConnector").val(0);
	$("#rxCable").val(0);
	$("#rxDiameter").val(0.8);
	$("#rxGain").val(40.9673);
	$("#rxSensetivity").val(-100);

    // Page has loaded now see if we have data in the URL
	if (/frequency/.test(window.location.href)) {
		$("#frequency").val(getURLParameter("frequency"));
		$("#distance").val(getURLParameter("distance"));
	
		$("#txConnector").val(getURLParameter("txConnectorLosses"));
		$("#txCable").val(getURLParameter("txCableLosses"));
		$("#txDiameter").val(getURLParameter("txAntennaDiameter"));
		$("#txGain").val(getURLParameter("txAntennaGain"));
		$("#txPower").val(getURLParameter("txPower"));
		
		$("#rxConnector").val(getURLParameter("rxConnectorLosses"));
		$("#rxCable").val(getURLParameter("rxCableLosses"));
		$("#rxDiameter").val(getURLParameter("rxAntennaDiameter"));
		$("#rxGain").val(getURLParameter("rxAntennaGain"));
		$("#rxSensetivity").val(getURLParameter("rxSensetivity"));
	}
		    
	$("#btnSubmit").click(function(){
		var frequency = $("#frequency").val();
		var distance = $("#distance").val();
		var txDiameter = $("#txDiameter").val();
		var txGain = $("#txGain").val();
		var txPower = $("#txPower").val();
		var txConnector = $("#txConnector").val();
		var txCable = $("#txCable").val();
		var rxDiameter = $("#rxDiameter").val();
		var rxGain = $("#rxGain").val();
		var rxSensetivity = $("#rxSensetivity").val();
		var rxConnector = $("#rxConnector").val();
		var rxCable = $("#rxCable").val();

		var getData = "?frequency=" + frequency + 
		"&distance=" + distance + 
		"&txAntennaDiameter=" + txDiameter + 
		"&rxAntennaDiameter=" + rxDiameter + 
		"&txAntennaGain=" + txGain + 
		"&rxAntennaGain=" + rxGain + 
		"&txPower=" + txPower + 
		"&rxSensetivity=" + rxSensetivity + 
		"&txConnectorLosses=" + txConnector + 
		"&rxConnectorLosses=" + rxConnector + 
		"&txCableLosses=" + txCable + 
		"&rxCableLosses=" + rxCable;

/*
	var getData = "?frequency=18" + "&distance=26.083" + "&txAntennaDiameter=1.8" + "&rxAntennaDiameter=0.8" + 
	"&txAntennaGain=48.0109" + "&rxAntennaGain=40.96725" + "&txPower=15" + "&rxSensetivity=-100" + 
	"&txConnectorLosses=0" + "&rxConnectorLosses=0" + "&txCableLosses=0" + "&rxCableLosses=0";
*/
		
		/*console.log(getData);*/
/*		18 26.083 1.8 0.8 48.0109 40.96725 15 -100 0 0 0 0   */
	    $.ajax({
		    url: "/cgi-bin/pathloss.py" + getData,
		    type: "GET",
		    beforeSend: function(){
                $("#loader").show();
            },
		    success: function(response){
   			    history.pushState({}, null, "http://www.predtest.uk/pathloss.html" + getData)

                $("#loader").hide();
                //console.log(response);
			    if ( (response != null) ) {
                	createPathloss(response);
                	document.getElementById('fresnelRadius').innerText = response.linkCalculations.fresnelRadius + 'm';
                	document.getElementById('farFieldStart').innerText = response.linkCalculations.farFieldStart + 'm';
                	document.getElementById('fadeMargin').innerText = response.linkCalculations.fadeMargin + 'db';
                	document.getElementById('linkAvailability').innerText = (parseFloat(response.linkCalculations.linkAvailability) * 100) + '%';
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
		var len = data.fresnelArray.length;
		var x = [];
		var y = [];
		var output = ""

		for (var i = 0; i < len; i++) {
			//x.push(data.fresnelArray[i].pointDistance);
			//y.push(data.fresnelArray[i].pointDiameter)
			var temp = "Point #" + i + "\tPoint Distance: " + data.fresnelArray[i].pointDistance + "\t\tPoint Radius: " + data.fresnelArray[i].pointRadius + "\n"
			output = output + temp;
		}	
		
		$("#fresnelOut").val(output);
		
	/*	var trace1 = {
		  x: x,
		  y: y,
		  fill: 'tozeroy',
		  type: 'scatter',
		  mode: 'none'
		};

		var x2 = [];
		var y2 = [];
		for (var i = 0; i < len; i++) {
			x2.push(data.fresnelArray[i].pointDistance);
			y2.push(0 - data.fresnelArray[i].pointDiameter)
		}	
		
		var trace2 = {
		  x: x2,
		  y: y2,
		  fill: 'tozeroy',
		  type: 'scatter',
		  mode: 'none'  
		};
		
		
		var layout = {
		  title: 'Fresnel Plot'
		};
		
		var data = [trace1, trace2];
		
		Plotly.newPlot('pathlossDiv', data, layout);
	*/
	}
});

//This function simply takes in power
// and returns the decibel value
function dbConvert(power)
{
    dB = 10*Math.log10( power/1);
    return dB;
}

//This function  takes in decibel
// and returns the power value
function powerConvert(dB)
{
    power = math.power(10,dB/10);
    return power;
}

function getURLParameter(name) {
  return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search) || [null, ''])[1].replace(/\+/g, '%20')) || null;
}
