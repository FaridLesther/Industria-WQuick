function isObjEmpty(obj) {
  for (var prop in obj) {
    if (obj.hasOwnProperty(prop)) return false;
  }
  return true;
}

function enviar(datos, metodo, objetos = {}, url) {
    let csrftoken = getCookie('csrftoken');
    fetch(url, {
        method: metodo,
        body: datos,
        headers: {"X-CSRFToken": csrftoken, 'X-Requested-With': 'XMLHttpRequest'},
    }).then(respuesta => respuesta.json())
      .then(respuesta => {
        if (!respuesta['resultado']) { 
          alerta(respuesta['mensaje'], 'red')
        }else {
          alerta(respuesta['mensaje'], 'green');
          if(!isObjEmpty(respuesta['datos'])){
            for (let i in objetos) {
              if(i == 'img'){
                if(objetos[i].length >= 1){
                  for(let j=0; j < objetos[i].length; j++){
                    objetos[i][j].src = respuesta['datos']['img']
                  }
                }
              }
            }
          }
        }
      })
      .catch(error => console.error('Error:', error));
}