// Novena función para calcular el porcentaje a la Champions League
const filas7 = document.querySelectorAll("#tablaCampeonVallad tbody tr");
const partidosTotales7 = 38; // Cambiado a 38 partidos en la temporada
const puntosPorGanar7 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFija7 = 67; // Ajusta este valor según tus necesidades
const equipos7 = [];
filas7.forEach((fila, indice) => {
    const equipo7 = fila.querySelector(`.fw-bold`).textContent;
    const partidosJugados7 = parseInt(fila.querySelector(`.camp-jug`).textContent);
    const puntosActuales7 = parseInt(fila.querySelector(`.camp-act`).textContent);
    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosParaChampions = Math.round((proximidadFija7 / 100) * partidosTotales7 * puntosPorGanar7);
    // Calcular la proximidad de ascenso
    const puntosQueFaltan7 = Math.max(0, puntosParaChampions - puntosActuales7);
    const proximidadDeChampions = Math.min(((puntosParaChampions - puntosQueFaltan7) / puntosParaChampions) * 100, 100);
    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesChampions = partidosTotales7 - partidosJugados7;
    const partidosGanadosMatematicos7 = Math.min(puntosActuales7 + partidosRestantesChampions * puntosPorGanar7, puntosParaChampions);
    const partidosGanadosPesimistas7 = Math.min(partidosGanadosMatematicos7 - 2, puntosParaChampions);
    const partidosGanadosOptimistas7 = Math.min(partidosGanadosMatematicos7 -7, puntosParaChampions);
    equipos7.push({
        equipo7,
        partidosJugados7,
        puntosActuales7,
        proximidadDeChampions,
        partidosGanadosMatematicos7,
        partidosGanadosOptimistas7,
        partidosGanadosPesimistas7
    });
});
// Ordenar los equipo7s7 por proximidad descendente
equipos7.sort((a, b) => b.proximidadDeChampions - a.proximidadDeChampions);
// Actualizar la tabla7 con los datos ordenados
const tabla7 = document.querySelector("#tablaCampeonVallad tbody");
tabla7.innerHTML = ""; // Limpiar la tabla7 antes de actualizar
equipos7.forEach((equipo7Data) => {
    const nuevaFila7 = document.createElement("tr");
    nuevaFila7.innerHTML = `
    <td class="fw-bold text-center">${equipo7Data.equipo7}</td>
    <td class="camp-jug fw-bold text-center">${equipo7Data.partidosJugados7}</td>
    <td class="camp-act fw-bold text-center">${equipo7Data.puntosActuales7}</td>
    <td class="camp-proxi fw-bold text-center">${equipo7Data.proximidadDeChampions.toFixed(2)}%</td>
    <td class="camp-mate fw-bold text-center">${equipo7Data.partidosGanadosMatematicos7}</td>
    <td class="camp-opti fw-bold text-center">${equipo7Data.partidosGanadosOptimistas7}</td>
    <td class="camp-pesi fw-bold text-center">${equipo7Data.partidosGanadosPesimistas7}</td>
    `;
    tabla7.appendChild(nuevaFila7);
});