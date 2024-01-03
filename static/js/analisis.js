document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('.table tbody tr');

    rows.forEach(row => {
        const ptosFav = parseInt(row.querySelector('.ptos-fav').textContent);
        const ptosCont = parseInt(row.querySelector('.ptos-cont').textContent);
        const ganados = parseInt(row.querySelector('.ganados').textContent);
        const perdidos = parseInt(row.querySelector('.perdidos').textContent);

        const partidosJugados = ganados + perdidos;
        row.querySelector('.jugados').textContent = partidosJugados;

        const diferenciaPuntos = ptosFav - ptosCont;
        row.querySelector('.dife').textContent = diferenciaPuntos;

        const puntos = ganados * 2 + perdidos;
        row.querySelector('.puntos').textContent = puntos;
    });

    const rowsArray = Array.from(rows);

    rowsArray.sort((a, b) => {
        const puntosA = parseInt(a.querySelector('.puntos').textContent);
        const puntosB = parseInt(b.querySelector('.puntos').textContent);
        return puntosB - puntosA; // Orden descendente por PTS
    });

    const tableBody = document.querySelector('.table tbody');
    tableBody.innerHTML = '';

    rowsArray.forEach(row => {
        tableBody.appendChild(row);
    });
});







