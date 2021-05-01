/*=================== Funcionalidades para los toats ===================*/
alertas = document.getElementsByClassName('alerta');
for (let i = 0; i < alertas.length; i++) {
    alertas[i].click();
}

function alerta(alerta, clase = 'red') {
    M.toast({
        html: alerta +
            '<button id = "Acerrar" onclick = "cerrarToats()" class="btn-flat toast-action">Cerrar</button>',
        classes: clase,
        displayLength: 5000
    });
}

cerrarToats = function () {
    var toastElement = document.querySelector('.toast');
    var toastInstance = M.Toast.getInstance(toastElement);
    toastInstance.dismiss();
}

/*=================== Al cargarse la pagina ===================*/
document.addEventListener('DOMContentLoaded', function () {
    M.AutoInit();
    /*=================== Funcionalidades para los dropdowns===================*/
    var drops = document.querySelectorAll('.auto-hover');
    var instances = M.Dropdown.init(drops, {
        coverTrigger: false,
        hover: true
    });

    var drops = document.querySelectorAll('.notificaciones');
    var instances = M.Dropdown.init(drops, {
        coverTrigger: false,
    });
    /*=================== Funcionalidades para los sliders ===================*/
    var sliders = document.querySelectorAll('.slider');
    var instances = M.Slider.init(sliders, {
        interval: 7000,
        height: 400,
        duration: 600
    });
    
    /*=================== Funcionalidades de los seleccionadores de fechas datepicker ===================*/
    var datas = document.querySelectorAll('.datepicker');
    var instances = M.Datepicker.init(datas, {
        format: "dd-mm-yyyy",
        firstDay: 1,
        minDate: new Date(),
        i18n: {
            months: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
                'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
            ],
            monthsShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul',
                'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
            ],
            weekdays: ['Domingo', 'Lunes', 'Martes',
                'Miércoles', 'Jueves', 'Viernes', 'Sabado'
            ],
            weekdaysShort: ['Domingo', 'Lunes', 'Martes',
                'Miércoles', 'Jueves', 'Viernes', 'Sábado'
            ],
            weekdaysAbbrev: ['D', 'L', 'M', 'M', 'J', 'V', 'S']
        }
    });
});

/*=================== Tabulador en las TextAreas ===================*/
function enableTab(id) {
    var el = document.getElementById(id);
    el.onkeydown = function(e) {
        if (e.key == 'Tab') { //la tecla tababulador ha sido presionada

            // obtener posición / selección de intercalación 
            var val = this.value,
                start = this.selectionStart,
                end = this.selectionEnd;

            // establecer el valor del área de texto en: texto antes del signo 
            //de intercalación + tabulación + texto después del intercalado
            this.value = val.substring(0, start) + '\t' + val.substring(end);

            // volver a poner el cursor en la posición correcta 
            this.selectionStart = this.selectionEnd = start + 1;

            // evitar que el foco sobre el textarea se pierda 
            return false;

        }
    };
}

/*=================== Altura variable en las TextAreas ===================*/
let area = document.querySelectorAll(".auto_scroll")
        
window.addEventListener("DOMContentLoaded", () => {
    area.forEach((elemento) => {
    elemento.style.height = `${elemento.scrollHeight}px`
    })
}) 