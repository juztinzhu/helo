
$(document).ready(
    function (){
	$("#input").change(handleFile);
	function handleFile(e) {
	    var files = e.target.files, f = files[0];
	    var reader = new FileReader();
	    var filename = genFileName(f.name);
	    reader.onload = function(e) {
		var data = e.target.result;
		workbook = XLSX.read(data, {type:'binary'});
		sheet = workbook.Sheets[workbook.SheetNames[0]];
		//parse xlsx file, extract cordinate
		cords = getCordsFromSheet(sheet);
		//cordinate to dec
		var decCords = cordsToDec(cords);
		//cordinate to gpx file
		var gpx = genGPX(decCords);
		download(filename, gpx);
	    };
	    reader.readAsBinaryString(f);
	    
	}

	function genFileName(orig) {
	    return RegExp(/(.*)\.(.*)/).exec(orig)[1]+".gpx"
	}


	function NamedGeoPoint(name, lon, lat) {
	    GeoPoint.call(this, lon, lat);
	    this.name = name;
	}

	NamedGeoPoint.prototype = Object.create(GeoPoint.prototype, {
	    name: {
		value: null, 
		enumerable: true, 
		configurable: true, 
		writable: true 
	    },
	});
	NamedGeoPoint.prototype.constructor = NamedGeoPoint;


	// class NamedGeoPoint extends GeoPoint {
	//     constructor(name, lon, lat){
	// 	super(lon, lat);
	// 	this.name = name;
	//     }
	// }

	function getCordsFromSheet(sheet) {
	    var rowMax = RegExp(/:\w([0-9]+)/).exec(sheet["!ref"])[1];
	    var cords = new Array();
	    var name = "";
	    for(var i = 1; i <= rowMax; ++i) {
		var cname = "A" + String(i);
		var clong = "B" + String(i);
		var clat = "C" + String(i);
		var celllon = sheet[clong];
		var celllat = sheet[clat];
		if ( !celllon || !celllat || !celllon["v"] || !celllat["v"])
		    continue;
		

		lon = celllon["v"].replace(/′/,"\'").replace(/″/,"\"");
		lat = celllat["v"].replace(/′/,"\'").replace(/″/,"\"");
		
		if (sheet[cname] && sheet[cname]["v"]){
		    name = sheet[cname]["v"];
		}
		else {
		    name += "_1";
		}

		var point = new NamedGeoPoint(name, lon, lat);

		console.log(name,lon,lat);
		cords.push(point);
	    }
	    return cords;    
	}

	function cordsToDec(points) {
	    var decCords = new Array();
	    for ( var i in points) {
		var dec = new Object();
		dec.lon = points[i].getLonDec();
		dec.lat = points[i].getLatDec();
		dec.name = points[i].name;
		decCords.push(dec);
	    }
	    return decCords;
	}

	function genGPX(cords) {
	    var xmlDoc = document.implementation.createDocument(null, "gpx");

	    for ( var i in cords) {
		var wpt = genwpt(xmlDoc, cords[i]);
		xmlDoc.documentElement.appendChild(wpt)
	    }
	    
	    return new XMLSerializer().serializeToString(xmlDoc.documentElement);
	}

	function genwpt(xmlDoc, cord) {
	    var wpt = xmlDoc.createElement('wpt');
	    wpt.setAttribute('lon', cord.lon);
	    wpt.setAttribute('lat', cord.lat);
	    
	    var time = xmlDoc.createElement('time');
	    time.textContent = "2018-01-25T14:17:38Z";
	    wpt.appendChild(time);
	    
	    var name = xmlDoc.createElement('name');
	    name.textContent = cord["name"];
	    console.log(cord["name"]);
	    wpt.appendChild(name);

	    var sym = xmlDoc.createElement('sym');
	    sym.textContent = "Flag, Blue";
	    wpt.appendChild(sym);

	    var type = xmlDoc.createElement('type');
	    type.textContent = "user";
	    wpt.appendChild(type);

	    
	    return wpt;
	}


	function download(filename, text) {
	    var element = document.createElement('a');
	    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
	    element.setAttribute('download', filename);

	    element.style.display = 'none';
	    document.body.appendChild(element);

	    element.click();

	    document.body.removeChild(element);
	}

    }
);

