let sesionTerminada = false;
let diaActual = '';
let fechaSesionActual = '';
let datosSesionActual = null;

const movilidadPorDia = {
    'Lunes': 'Balanceos adelante/atrás y laterales (15 reps), rotaciones de cadera (10 c/u) y rodillas al pecho (10 pasos).',
    'Martes': 'Dislocaciones de hombro (15 reps), tirones horizontales con banda (15 reps) y dislocaciones unilaterales (10 c/u).',
    'Miercoles': 'Cruces de brazos en el aire (20 reps) y empujes frontales con banda (15 reps).',
    'Jueves': 'Balanceos adelante/atrás y laterales (15 reps) y rotaciones de cadera (10 c/u).',
    'Viernes': 'Círculos amplios con los brazos (20 reps) y face pulls livianos con banda (15 reps).'
};

window.onload = function() { cargarSemanasDisponibles(); };

function cargarSemanasDisponibles() {
    fetch('/semanas')
        .then(response => response.json())
        .then(data => {
            const selector = document.getElementById('selector-semana');
            selector.innerHTML = '';
            data.forEach(sem => {
                let option = document.createElement('option');
                option.value = sem.valor;
                option.text = sem.texto;
                selector.appendChild(option);
            });
        });
}

function irInicio() { location.reload(); }
function validarEntero(input) { input.value = input.value.replace(/[^0-9]/g, ''); }
function validarDecimal(input) {
    let valor = input.value.replace(/,/g, '.').replace(/[^0-9.]/g, '');
    let partes = valor.split('.');
    if (partes.length > 2) valor = partes[0] + '.' + partes.slice(1).join('');
    if (partes.length > 1 && partes[1].length > 1) valor = partes[0] + '.' + partes[1].substring(0, 1);
    input.value = valor;
}

function recargarDia() { if (diaActual) cargarRutina(diaActual); }

function guardarDatos(ejId, nSerie) {
    const reps = document.getElementById(`reps-${ejId}-${nSerie}`).value;
    const peso = document.getElementById(`peso-${ejId}-${nSerie}`).value;
    if (!reps || !peso) return;

    fetch('/guardar_serie', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            fecha: fechaSesionActual, ejercicio_id: ejId, numero_serie: nSerie, reps: reps, peso: peso
        })
    });
}

function toggleSesion() {
    sesionTerminada = !sesionTerminada;
    renderizarRutina();
}

function cambiarVariante(indexEjercicio, nuevoId) {
    datosSesionActual.rutina[indexEjercicio].id_seleccionado = parseInt(nuevoId);
    renderizarRutina();
}

function toggleMovilidad() {
    const box = document.getElementById('box-movilidad');
    box.classList.toggle('completado');
    const key = `movilidad_${diaActual}_${fechaSesionActual}`;
    localStorage.setItem(key, box.classList.contains('completado'));
}

function renderizarRutina() {
    let html = `<h3>Rutina del ${diaActual}</h3>`;
    html += `<div class="fecha-texto">Fecha de entrenamiento: ${fechaSesionActual}</div>`;
    
    const keyMovilidad = `movilidad_${diaActual}_${fechaSesionActual}`;
    const claseCompletado = localStorage.getItem(keyMovilidad) === 'true' ? 'completado' : '';

    html += `<div id="box-movilidad" class="box-movilidad ${claseCompletado}" onclick="toggleMovilidad()">
        <strong style="display: block; margin-bottom: 5px;">Movilidad Articular (2 vueltas x 15 reps):</strong>
        ${movilidadPorDia[diaActual] || 'Realizar movilidad general.'}
    </div>`;

    let grupoActual = '';

    datosSesionActual.rutina.forEach((ej, index) => {
        if (ej.grupo_muscular !== grupoActual) {
            html += `<div style="background-color: #343a40; color: white; padding: 8px; margin-top: 25px; margin-bottom: 15px; border-radius: 4px; text-align: center; text-transform: uppercase; font-size: 18px;">${ej.grupo_muscular}</div>`;
            grupoActual = ej.grupo_muscular;
        }

        html += `<div class="ejercicio">`;
        
        if (!ej.id_seleccionado) {
            ej.id_seleccionado = ej.ejercicio_id;
            ej.variantes.forEach(v => {
                if (datosSesionActual.historial.some(h => h.ejercicio_id === v.id)) {
                    ej.id_seleccionado = v.id;
                }
            });
        }

        if (ej.variantes.length > 1) {
            html += `<select class="select-variante" onchange="cambiarVariante(${index}, this.value)" ${sesionTerminada ? 'disabled' : ''}>`;
            ej.variantes.forEach(v => {
                const selected = v.id == ej.id_seleccionado ? 'selected' : '';
                html += `<option value="${v.id}" ${selected}>${v.nombre}</option>`;
            });
            html += `</select>`;
        } else {
            html += `<h4>${ej.nombre}</h4>`;
        }

        if (ej.es_calentamiento === 1) {
            html += `<p style="font-weight: bold; margin-bottom: 5px;">Series de aproximacion</p>`;
            
            if (ej.notas) html += `<p style="margin-top: 0; margin-bottom: 10px;"><small>${ej.notas}</small></p>`;

            for (let i = 1; i <= 2; i++) {
                let nSerie = 100 + i;
                const datoPrevio = datosSesionActual.historial.find(h => h.ejercicio_id == ej.id_seleccionado && h.numero_serie === nSerie);
                const rVal = datoPrevio ? datoPrevio.repeticiones : '';
                const pVal = datoPrevio ? datoPrevio.peso : '';
                const disabled = sesionTerminada ? 'disabled' : '';

                html += `<div class="serie-row">
                    <span>A${i}:</span>
                    <input type="text" id="reps-${ej.id_seleccionado}-${nSerie}" class="input-box" placeholder="Reps" 
                        inputmode="numeric" oninput="validarEntero(this)" onblur="guardarDatos(${ej.id_seleccionado}, ${nSerie})" value="${rVal}" ${disabled}>
                    <input type="text" id="peso-${ej.id_seleccionado}-${nSerie}" class="input-box" placeholder="Kilos" 
                        inputmode="decimal" oninput="validarDecimal(this)" onblur="guardarDatos(${ej.id_seleccionado}, ${nSerie})" value="${pVal}" ${disabled}>
                </div>`;
            }
            html += `<p style="font-weight: bold; margin-top: 15px; margin-bottom: 5px;">Series efectivas</p>`;
        } else if (ej.notas) {
            html += `<p style="margin-top: 0; margin-bottom: 5px;"><small>${ej.notas}</small></p>`;
        }

        html += `<p style="margin-top: 0;">Objetivo: ${ej.series_objetivo} series de ${ej.reps_rango}</p>`;
        
        for (let i = 1; i <= ej.series_objetivo; i++) {
            const datoPrevio = datosSesionActual.historial.find(h => h.ejercicio_id == ej.id_seleccionado && h.numero_serie === i);
            const rVal = datoPrevio ? datoPrevio.repeticiones : '';
            const pVal = datoPrevio ? datoPrevio.peso : '';
            const disabled = sesionTerminada ? 'disabled' : '';

            html += `<div class="serie-row">
                <span>${i}:</span>
                <input type="text" id="reps-${ej.id_seleccionado}-${i}" class="input-box" placeholder="Reps" 
                    inputmode="numeric" oninput="validarEntero(this)" onblur="guardarDatos(${ej.id_seleccionado}, ${i})" value="${rVal}" ${disabled}>
                <input type="text" id="peso-${ej.id_seleccionado}-${i}" class="input-box" placeholder="Kilos" 
                    inputmode="decimal" oninput="validarDecimal(this)" onblur="guardarDatos(${ej.id_seleccionado}, ${i})" value="${pVal}" ${disabled}>
            </div>`;
        }
        html += `</div>`;
    });
    
    let textoBoton = sesionTerminada ? 'EDITAR SESION' : 'TERMINAR SESION';
    let colorBoton = sesionTerminada ? '#6c757d' : '#dc3545';
    html += `<button id="btn-sesion" class="btn-accion" style="background-color: ${colorBoton};" onclick="toggleSesion()">${textoBoton}</button>`;
    
    document.getElementById('rutina').innerHTML = html;
}

function cargarRutina(dia) {
    diaActual = dia;
    const semanasAtras = document.getElementById('selector-semana').value;
    fetch('/rutina/' + dia + '/' + semanasAtras)
        .then(response => response.json())
        .then(res => {
            fechaSesionActual = res.fecha_sesion;
            datosSesionActual = res;
            sesionTerminada = false;
            renderizarRutina();
        });
}