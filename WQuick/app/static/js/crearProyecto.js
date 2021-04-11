let form = document.querySelector('.form-register');
let progressOptions = document.querySelectorAll('.progressbar__option');

form.addEventListener('click', function(e) {
    let titulo = document.getElementById('txt_titulo').value;
    let descripcion = document.getElementById('txt-descripcion').value;
    
    let element = e.target;

    let crear = document.getElementById('btnCrear');

    crear.onclick = (evento)=>{
        if(titulo == '' || descripcion == ''){
            evento.preventDefault();
        }
    }

    if(!isNaN((element.dataset.to_step - 1))){
        if((element.dataset.to_step - 1) == 2 && (titulo == '' || descripcion == '')){
            if(titulo == ''){
                document.getElementById("alert_titulo").style.display = "inline-flex";
            }else{
                document.getElementById("alert_titulo").style.display = "none";
            }
            if(descripcion == ''){
                document.getElementById("alert_descripcion").style.display = "inline-flex";
            }else{
                document.getElementById("alert_descripcion").style.display = "none";
            }
        }else{
            let categoria = document.querySelectorAll('input[type="radio"]');
            categoria.forEach(opcion =>{
                //si la opcion recorrida esta seleccionada mostramos esa opcion
                if(opcion.checked){
                    let tipo = document.getElementById('txt_tipo');
                    tipo.value = opcion.value;
                }
            });

            document.getElementById("alert_descripcion").style.display = "none";
            document.getElementById("alert_titulo").style.display = "none";
            let isButtonNext = element.classList.contains('step__button--next');
            let isButtonBack = element.classList.contains('step__button--back');
            if (isButtonNext || isButtonBack) {
                let currentStep = document.getElementById('step-' + element.dataset.step);
                let jumpStep = document.getElementById('step-' + element.dataset.to_step);
                currentStep.addEventListener('animationend', function callback() {
                    currentStep.classList.remove('active');
                    jumpStep.classList.add('active');
                    if (isButtonNext) {
                        currentStep.classList.add('to-left');
                        progressOptions[element.dataset.to_step - 1].classList.add('active');
                    } else {
                        jumpStep.classList.remove('to-left');
                        progressOptions[element.dataset.step - 1].classList.remove('active');
                    }
                    currentStep.removeEventListener('animationend', callback);
                });
                currentStep.classList.add('inactive');
                jumpStep.classList.remove('inactive');
            }
        }
    }
});
