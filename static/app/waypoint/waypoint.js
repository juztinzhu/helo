var rABS = true; // true: readAsBinaryString ; false: readAsArrayBuffer

$(document).ready(function (){
    $("#input").change(handleFile);
}
		 );

function handleFile(e) {
    var files = e.target.files, f = files[0];
    var reader = new FileReader();
    reader.onload = function(e) {
	
	var data = e.target.result;
	if(!rABS) data = new Uint8Array(data);
	workbook = XLSX.read(data, {type: rABS ? 'binary' : 'array'});
	

	/* DO SOMETHING WITH workbook HERE */
    };
    if(rABS)
	reader.readAsBinaryString(f);
    else
	reader.readAsArrayBuffer(f);
}


