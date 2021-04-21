const btnGuardarI = document.getElementById('btn-guardari');
// funcion que válida la imagen que se subira de de perfil de usuario
btnGuardarI.onclick = (evento) => {
    evento.preventDefault()
    var txtImagen = document.getElementById('txt-imagen');
    //se comprueba que la imagen sea diferente a la imagen actual del usuario
    // si la imagen es la misma se borra y no se realiza ninguna accion
    // y se deshabilita el boton de guardar
    if ('perfil/' + txtImagen.value == imagenActual) {
        txtImagen.value = '';
        alerta('La imagen que intenta guardar es la imagen actual de perfil', "red");
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
            alerta("Extensión de archivo imagen no valida", "red");
            txtImagen.value = '';
            btnGuardarI.style.display = 'none';
            document.getElementById('id_foto').value = '';
            return;
        }

        if ((document.getElementById('id_foto').files[0].size / 1048576) > tamano) {
            alerta("El archivo no puede superar los " + tamano + "MB", 'red')
            document.getElementById(all.id).value = "";
            return;
        }
  
        let datos = new FormData();  
        let imagen = document.getElementById('id_foto')

        let imagenNavbar = document.getElementById('avatar');
        if(imagenNavbar == null){
            imagenNavbar = document.getElementsByName('avatar')[0];
        }

        let imagenPerfil = {'img': [document.getElementById('userImagen'), imagenNavbar]};
        datos.append('imagen', imagen.files[0])
        enviar(datos, 'POST', imagenPerfil, '/perfil');
        btnGuardarI.style.display = 'none';
        document.getElementById('id_foto').value = '';
        txtImagen.value = '';
    }

}