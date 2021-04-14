const btnGuardarI = document.getElementById('btn-guardari');
// funcion que válida la imagen que se subira de de perfil de usuario
btnGuardarI.onclick = (evento) => {
    evento.preventDefault();
    txtImagen = document.getElementById('txt-imagen');
    //se comprueba que la imagen sea diferente a la imagen actual del usuario
    // si la imagen es la misma se borra y no se realiza ninguna accion
    // y se deshabilita el boton de guardar
    if ('perfil/' + txtImagen.value == imagenActual) {
        txtImagen.value = '';
        alert('La imagen que intenta guardar es la imagen actual de perfil');
        btnGuardarI.style.display = 'none';
        document.getElementById('id_foto').value = '';
        return; // Si la imagen es la misma de perfil actual ya no chequeo lo de abajo.
    } else {
        //EXTENSIONES Y TAMANO PERMITIDO.
        var extensiones_permitidas = [".png", ".jpg",".JPG", ".jpeg", ".gif"];
        var tamano = 8; // EXPRESADO EN MB.
        var rutayarchivo = document.getElementById('id_foto').value;
        var ultimo_punto = document.getElementById('id_foto').value.lastIndexOf(".");
        var extension = rutayarchivo.slice(ultimo_punto, rutayarchivo.length);

        if (extensiones_permitidas.indexOf(extension) == -1) {
            evento.preventDefault();
            alert("Extensión de archivo imagen no valida");
            txtImagen.value = '';
            btnGuardarI.style.display = 'none';
            document.getElementById('id_foto').value = '';
            return;
        }

        if ((document.getElementById('id_foto').files[0].size / 1048576) > tamano) {
            evento.preventDefault();
            alert("El archivo no puede superar los " + tamano + "MB");
            document.getElementById(all.id).value = "";
            return;
        }
        document.getElementById('fileinfo').submit();  
        
    }

}