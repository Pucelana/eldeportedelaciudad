const filas2 = document.querySelectorAll("#tablaDescUemc tbody tr");
const partidosTotales2 = 34; // Total de partidos en la temporada
const partidosPorGanar2 = 1; // Cantidad de puntos por partido ganado

const equiposDesc = [];

filas2.forEach((fila, indice) => {
    const equipo = fila.querySelector(`.fw-bold`).textContent;
    const partidosJugados = parseInt(fila.querySelector(`.play-jug`).textContent);
    const puntosActuales = parseInt(fila.querySelector(`.play-act`).textContent);

    const partidosRestantes = partidosTotales2 - partidosJugados;
    const partidosGanadosNecesarios = Math.ceil((partidosTotales2 * 0.5) + 1);

    const partidosGanadosMatematicos = Math.min(partidosRestantes * partidosPorGanar2 + puntosActuales, partidosTotales2);
    const partidosGanadosOptimistas = Math.min(partidosGanadosMatematicos - 8, partidosTotales2);
    const partidosGanadosPesimistas = Math.min(partidosGanadosMatematicos - 5, partidosTotales2)
    const proximidadAscenso = (partidosGanadosMatematicos / partidosGanadosNecesarios) * 10;

    equiposDesc.push({
        equipo,
        partidosJugados,
        puntosActuales,
        proximidadAscenso,
        partidosGanadosMatematicos,
        partidosGanadosOptimistas,
        partidosGanadosPesimistas
    });
});

// Ordenar los equiposDesc por proximidad descendente
equiposDesc.sort((a, b) => b.proximidadAscenso - a.proximidadAscenso);
// Actualizar la tabla con los datos ordenados
const tabla2 = document.querySelector("#tablaDescUemc tbody");
tabla2.innerHTML = ""; // Limpiar la tabla antes de actualizar
equiposDesc.forEach((equipoData) => {
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
    tabla2.appendChild(nuevaFila);
});