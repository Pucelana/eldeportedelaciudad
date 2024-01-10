// Primera función para calcular la clasificación y oredenar automaticamente
function calcularEstadisticas() {
    const tablaDatos = document.getElementById('tablaClasificacion');
    const filasDatos = Array.from(tablaDatos.querySelectorAll('tbody tr'));
    filasDatos.forEach(row => {
        const ptosFav = parseInt(row.querySelector('.favor').textContent);
        const ptosCont = parseInt(row.querySelector('.contra').textContent);
        const ganados = parseInt(row.querySelector('.ganados').textContent);
        const perdidos = parseInt(row.querySelector('.perdidos').textContent);
        const partidosJugados = ganados + perdidos;
        row.querySelector('.jugados').textContent = partidosJugados;
        const diferenciaPuntos = ptosFav - ptosCont;
        row.querySelector('.dife').textContent = diferenciaPuntos;
        const puntos = ganados * 2 + perdidos;
        row.querySelector('.puntos').textContent = puntos;
    });
    // Ordenar filas de datos según los puntos (PTS) de mayor a menor
    filasDatos.sort((a, b) => {
        const puntosA = parseInt(a.querySelector('.puntos').textContent);
        const puntosB = parseInt(b.querySelector('.puntos').textContent);
        const difPuntosA = parseInt(a.querySelector('.dife').textContent);
        const difPuntosB = parseInt(b.querySelector('.dife').textContent);
        if (puntosB !== puntosA) {
            return puntosB - puntosA; // Ordenar por puntos de mayor a menor
        } else {
            return difPuntosB - difPuntosA; // Si los puntos son iguales, ordenar por diferencia de puntos
        }
    });
    // Limpiar y reinsertar las filas ordenadas
    const tbody = tablaDatos.querySelector('tbody');
    tbody.innerHTML = '';
    filasDatos.forEach(fila => {
        tbody.appendChild(fila);
    });
  }
  document.addEventListener('DOMContentLoaded', function() {
    calcularEstadisticas();
  });
// Segunda función para calcular el porcentaje al ascenso

const filas = document.querySelectorAll("#tablaAscenso tbody tr");
const partidosTotales = 34; // Total de partidos en la temporada
const partidosPorGanar = 1; // Cantidad de puntos por partido ganado

const equipos = [];

filas.forEach((fila, indice) => {
    const equipo = fila.querySelector(`.fw-bold`).textContent;
    const partidosJugados = parseInt(fila.querySelector(`.jugados1`).textContent);
    const puntosActuales = parseInt(fila.querySelector(`.pts-act1`).textContent);

    const partidosRestantes = partidosTotales - partidosJugados;
    const partidosGanadosNecesarios = Math.ceil((partidosTotales * 0.5) + 1);

    const partidosGanadosMatematicos = Math.min(partidosRestantes * partidosPorGanar + puntosActuales, partidosTotales);
    const partidosGanadosOptimistas = Math.min(partidosGanadosMatematicos - 4, partidosTotales);
    const partidosGanadosPesimistas = Math.min(partidosGanadosMatematicos - 2, partidosTotales)
    const proximidadAscenso = (partidosGanadosMatematicos / partidosGanadosNecesarios) * 10;

    equipos.push({
        equipo,
        partidosJugados,
        puntosActuales,
        proximidadAscenso,
        partidosGanadosMatematicos,
        partidosGanadosOptimistas,
        partidosGanadosPesimistas
    });
});

// Ordenar los equipos por proximidad descendente
equipos.sort((a, b) => b.proximidadAscenso - a.proximidadAscenso);
// Actualizar la tabla con los datos ordenados
const tabla = document.querySelector("#tablaAscenso tbody");
tabla.innerHTML = ""; // Limpiar la tabla antes de actualizar
equipos.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    nuevaFila.innerHTML = `
    <td class="fw-bold text-center">${equipoData.equipo}</td>
    <td class="jugados1 fw-bold text-center">${equipoData.partidosJugados}</td>
    <td class="pts-act1 fw-bold text-center">${equipoData.puntosActuales}</td>
    <td class="proxi1 fw-bold text-center">${equipoData.proximidadAscenso.toFixed(2)}%</td>
    <td class="pts-mate1 fw-bold text-center">${equipoData.partidosGanadosMatematicos}</td>
    <td class="pts-opti1 fw-bold text-center">${equipoData.partidosGanadosOptimistas}</td>
    <td class="pts-pesi1 fw-bold text-center">${equipoData.partidosGanadosPesimistas}</td>
    `;
    tabla.appendChild(nuevaFila);
});

// Tercera función playoff y ordenar automaticamente
const filas1 = document.querySelectorAll("#tablaPlayUemc tbody tr");
const partidosTotales1 = 34; // Total de partidos en la temporada
const partidosPorGanar1 = 1; // Cantidad de puntos por partido ganado

const equiposPlay = [];

filas1.forEach((fila, indice) => {
    const equipo = fila.querySelector(`.fw-bold`).textContent;
    const partidosJugados = parseInt(fila.querySelector(`.play-jug`).textContent);
    const puntosActuales = parseInt(fila.querySelector(`.play-act`).textContent);

    const partidosRestantes = partidosTotales1 - partidosJugados;
    const partidosGanadosNecesarios = Math.ceil((partidosTotales1 * 0.5) + 1);

    const partidosGanadosMatematicos = Math.min(partidosRestantes * partidosPorGanar1 + puntosActuales, partidosTotales1);
    const partidosGanadosOptimistas = Math.min(partidosGanadosMatematicos - 8, partidosTotales1);
    const partidosGanadosPesimistas = Math.min(partidosGanadosMatematicos - 5, partidosTotales1)
    const proximidadAscenso = (partidosGanadosMatematicos / partidosGanadosNecesarios) * 10;

    equiposPlay.push({
        equipo,
        partidosJugados,
        puntosActuales,
        proximidadAscenso,
        partidosGanadosMatematicos,
        partidosGanadosOptimistas,
        partidosGanadosPesimistas
    });
});

// Ordenar los equiposPlay por proximidad descendente
equiposPlay.sort((a, b) => b.proximidadAscenso - a.proximidadAscenso);
// Actualizar la tabla con los datos ordenados
const tabla1 = document.querySelector("#tablaPlayUemc tbody");
tabla1.innerHTML = ""; // Limpiar la tabla antes de actualizar
equiposPlay.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    nuevaFila.innerHTML = `
    <td class="fw-bold text-center">${equipoData.equipo}</td>
    <td class="play-jug fw-bold text-center">${equipoData.partidosJugados}</td>
    <td class="play-act fw-bold text-center">${equipoData.puntosActuales}</td>
    <td class="play-prox fw-bold text-center">${equipoData.proximidadAscenso.toFixed(2)}%</td>
    <td class="play-mate fw-bold text-center">${equipoData.partidosGanadosMatematicos}</td>
    <td class="play-opti fw-bold text-center">${equipoData.partidosGanadosOptimistas}</td>
    <td class="play-pesi fw-bold text-center">${equipoData.partidosGanadosPesimistas}</td>
    `;
    tabla1.appendChild(nuevaFila);
});

// Cuarta función descenso y ordenar automaticamente










