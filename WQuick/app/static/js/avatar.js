function generarLetra(){
	var letras = ["a","b","c","d","e","f","2","3","4","5","6","7","8","9"];
	var numero = (Math.random()*15).toFixed(0);
	return letras[numero];
}
	
function colorHEX(){
	var coolor = "";
	for(var i=0;i<6;i++){
		coolor = coolor + generarLetra() ;
	}
	return "#" + coolor;
}

function generateAvatar(
    text,
    foregroundColor = "white",
    backgroundColor = "black"
  ) {
    backgroundColor = colorHEX();
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
  
    canvas.width = 150;
    canvas.height = 150;
  
    // Draw background
    context.fillStyle = backgroundColor;
    context.fillRect(0, 0, canvas.width, canvas.height);
  
    // Draw text
    context.font = "bold 100px Assistant";
    context.fillStyle = foregroundColor;
    context.textAlign = "center";
    context.textBaseline = "middle";
    context.fillText(text, canvas.width / 2, canvas.height / 2);
  
    return canvas.toDataURL("image/png");
  }