/*const multipleItemCarousel=document.querySelector('#carouselExampleControls')
if(window.matchMedia("(min-width:320px)").matches){
    const carousel = new bootstrap.Carousel(multipleItemCarousel,
    {
        interval: false
    })
    var carouselWidth=$('.carousel-inner')[0].scrollWidth;
    var cardWidth=$('.carousel-item').width();
    var scrollPosition=0;

    $('.carousel-control-next').on('click',function(){
        if(scrollPosition < (carouselWidth - (cardWidth*2))){
            console.log('next');
            scrollPosition=scrollPosition+cardWidth;
            $('.carousel-inner').animate({scrollLeft: scrollPosition},600);
        }
    });
    $('.carousel-control-prev').on('click',function(){
        if(scrollPosition > 0){
            console.log('prev');
            scrollPosition=scrollPosition - cardWidth;
            $('.carousel-inner').animate({scrollLeft: scrollPosition},600);
        }
    });
}else{
    console.error('Elemento no encontrado con el ID carouselExampleControls');
    $(multipleItemCarousel).addClass('slide');
}*/
const multipleItemCarousel = document.querySelector('#carouselExampleControls');

if (window.matchMedia("(min-width:320px)").matches) {
    // Inicializar el carrusel
    const carousel = new bootstrap.Carousel(multipleItemCarousel, {
        interval: false
    });

    // Detectar gestos táctiles utilizando Hammer.js
    var mc = new Hammer(multipleItemCarousel);
    mc.on("swipeleft", function () {
        carousel.next(); // Avanzar al siguiente elemento del carrusel
    });
    mc.on("swiperight", function () {
        carousel.prev(); // Retroceder al elemento anterior del carrusel
    });
} else {
    // Inicializar el carrusel con flechas
    const carousel = new bootstrap.Carousel(multipleItemCarousel, {
        interval: false
    });

    // Agregar eventos de clic a las flechas
    $('.carousel-control-next').on('click', function () {
        carousel.next(); // Avanzar al siguiente elemento del carrusel
    });
    $('.carousel-control-prev').on('click', function () {
        carousel.prev(); // Retroceder al elemento anterior del carrusel
    });
}

