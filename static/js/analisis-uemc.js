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
/*const totalEquipos = 18; // Total de equipos en la liga*/
const partidosTotales = 34; // Total de partidos en la temporada
const puntosPorVictoria = 2;
const puntosPorDerrota = 1;
// Crear un array para almacenar los datos de cada equipo
const equipos = [];
filas.forEach((fila, indice) => {
    // Obtener datos de la fila actual
    const equipo = fila.querySelector(`.fw-bold`).textContent; 
    const partidosJugados = parseInt(fila.querySelector(`.jugados1`).textContent);
    const puntosActuales = parseInt(fila.querySelector(`.pts-act1`).textContent);
    // Calcular puntos por partido y puntos restantes para la temporada
    const partidosRestantes = partidosTotales - partidosJugados;
    const puntosMatematicos = puntosActuales + (partidosRestantes * puntosPorVictoria);
    // Calcular escenarios optimista y pesimista
    const puntosOptimistas = puntosActuales + (partidosRestantes * puntosPorVictoria);
    const puntosPesimistas = puntosActuales + (partidosRestantes * puntosPorDerrota);
    // Calcular la proximidad al ascenso directo en porcentaje
    const puntosAscensoDirecto = partidosTotales * puntosPorVictoria;
    const proximidadAscenso = (puntosMatematicos / puntosAscensoDirecto) * 100;
    // Guardar los datos del equipo en el array 'equipos'
    equipos.push({ equipo, proximidadAscenso, puntosMatematicos, puntosOptimistas, puntosPesimistas, partidosJugados, puntosActuales });
});
// Ordenar los equipos por proximidad descendente
equipos.sort((a, b) => b.proximidadAscenso - a.proximidadAscenso);
// Actualizar la tabla con los datos ordenados
const tabla = document.querySelector("#tablaAscenso tbody");
tabla.innerHTML = ""; // Limpiar la tabla antes de actualizar
equipos.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    nuevaFila.innerHTML = `
    <td class="fw-bold">${equipoData.equipo}</td>
    <td class="jugados1 fw-bold">${equipoData.partidosJugados}</td>
    <td class="pts-act1 fw-bold">${equipoData.puntosActuales}</td>
    <td class="proxi1 fw-bold">${equipoData.proximidadAscenso.toFixed(2)}%</td>
    <td class="pts-mate1 fw-bold">${equipoData.puntosMatematicos}</td>
    <td class="pts-opti1 fw-bold">${equipoData.puntosOptimistas}</td>
    <td class="pts-pesi1 fw-bold">${equipoData.puntosPesimistas}</td>
    `;
    tabla.appendChild(nuevaFila);
});
// Tercera función playoff y ordenar automaticamente










