$(document).ready(function () {

  // $('#sidebarCollapse').on('click', function () {
  //   $('#sidebar').toggleClass('active');
  // });

  $("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
  });

  // Carousel Full Screen
  var $item = $('.carousel-item');
  var $mapItem = $('#map');
  var $wHeight = $(window).height() - $('#nav-top').outerHeight();

  $item.eq(0).addClass('active');
  $item.height($wHeight);
  $item.addClass('full-screen');

  $mapItem.height($wHeight);

  $(window).on('resize', function (){
    $wHeight = $(window).height() - $('#nav-top').outerHeight();
    $item.height($wHeight);
    $mapItem.height($wHeight);
  });

  $('.carousel img').each(function() {
    var $src = $(this).attr('src');
    var $color = $(this).attr('data-color');
    $(this).parent().css({
      'background-image' : 'url(' + $src + ')',
      'background-color' : $color
    });
    $(this).remove();
  });

  $('.carousel').carousel({
    interval: 6000,
    pause: "false"
  });

});
