 /* Para que el texto no aparezca entero y se pueda usar leer mas */
 var comments = document.getElementsByClassName('card_coments');
 for (var i = 0; i < comments.length; i++) {
   var comment = comments[i];
   var commentText = comment.getElementsByClassName('coment_text')[0];
   var readMoreLink = comment.getElementsByClassName('leer_mas')[0];
 
   // Obtener el texto del comentario
 
   // Contar las palabras en el texto del comentario
   var palabras = commentText.textContent.split(' ');
 
   // Establecer la longitud mínima para mostrar el enlace "Leer más"
   var longitudMinima = 50;
 
   if (palabras.length > longitudMinima) {
     readMoreLink.style.display = 'inline';
 
     readMoreLink.addEventListener('click', function(e) {
       e.preventDefault();
       comment.classList.toggle('expand');
     });
   } else {
     readMoreLink.style.display = 'none';
   }
 }
// Mostrar formulario para crear partidos
 function mostrarFormulario(){
  document.getElementById('form_partidos_uemc').style.display='block';
}
function mostrarFormularioPonce(){
  document.getElementById('form_partidos_ponce').style.display='block';
}
function mostrarFormularioAliados(){
  document.getElementById('form_partidos_aliados').style.display='block';
}
function mostrarFormularioValladolid(){
  document.getElementById('form_partidos_valladolid').style.display='block';
}
function mostrarFormularioPromesas(){
  document.getElementById('form_partidos_promesas').style.display='block';
}
function mostrarFormularioSimancas(){
  document.getElementById('form_partidos_promesas').style.display='block';
}
// Abrir y cerrar las jornadas de calendario_uemc
function toggleTabla(element, nombre) {
  event.preventDefault();
  var tabla = element.parentNode.parentNode.querySelector('.tabla_jornadas tbody');
  if (tabla.style.display === 'none') {
    tabla.style.display = 'table-row-group';
    element.innerHTML = 'Ocultar';
  } else {
    tabla.style.display = 'none';
    element.innerHTML = 'Ver';
  }
}
