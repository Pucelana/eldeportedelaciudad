const multipleItemCarousel=document.querySelector('#carouselExampleControls')
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
            $('.carousel-inner').animate({scrollLeft: scrollPosition},300);
        }
    });
    $('.carousel-control-prev').on('click',function(){
        if(scrollPosition > 0){
            console.log('prev');
            scrollPosition=scrollPosition - cardWidth;
            $('.carousel-inner').animate({scrollLeft: scrollPosition},300);
        }
    });
}else{
    console.error('Elemento no encontrado con el ID carouselExampleControls');
    $(multipleItemCarousel).addClass('slide');
}