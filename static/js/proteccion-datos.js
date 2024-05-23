// Obtener elementos del DOM
const avisoLegalLink = document.getElementById('aviso-legal-link');
const politicaPrivacidadLink = document.getElementById('politica-privacidad-link');
const politicaCookiesLink = document.getElementById('politica-cookies-link');

const avisoLegalModal = document.getElementById('aviso-legal-modal');
const politicaPrivacidadModal = document.getElementById('politica-privacidad-modal');
const politicaCookiesModal = document.getElementById('politica-cookies-modal');

const closeAvisoLegal = document.getElementById('close-aviso-legal');
const closePoliticaPrivacidad = document.getElementById('close-politica-privacidad');
const closePoliticaCookies = document.getElementById('close-politica-cookies');

// Función para abrir un modal
function openModal(modal) {
    modal.style.display = 'block';
}

// Función para cerrar un modal
function closeModal(modal) {
    modal.style.display = 'none';
}

// Abrir modales al hacer clic en los enlaces
avisoLegalLink.onclick = function() {
    openModal(avisoLegalModal);
    return false; // Evitar que el enlace navegue
}

politicaPrivacidadLink.onclick = function() {
    openModal(politicaPrivacidadModal);
    return false;
}

politicaCookiesLink.onclick = function() {
    openModal(politicaCookiesModal);
    return false;
}

// Cerrar modales al hacer clic en el botón de cerrar
closeAvisoLegal.onclick = function() {
    closeModal(avisoLegalModal);
}

closePoliticaPrivacidad.onclick = function() {
    closeModal(politicaPrivacidadModal);
}

closePoliticaCookies.onclick = function() {
    closeModal(politicaCookiesModal);
}

// Cerrar modales al hacer clic fuera del contenido del modal
window.onclick = function(event) {
    if (event.target == avisoLegalModal) {
        closeModal(avisoLegalModal);
    } else if (event.target == politicaPrivacidadModal) {
        closeModal(politicaPrivacidadModal);
    } else if (event.target == politicaCookiesModal) {
        closeModal(politicaCookiesModal);
    }
}