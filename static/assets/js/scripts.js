$(window).on("load", function() {
    "use strict";


  //  ============= MOBILE RESPONSIVE MENU ===============

  if ($('nav ul ul').length) {
    $("nav ul ul").parent().addClass("menu-has-items");
  };
  if($('.menu-btn').length) {
    $(".menu-btn").on("click", function(){
      $(this).toggleClass("active");
      $(".responsive-mobile-menu").toggleClass("active");
    });
    $(".responsive-mobile-menu ul ul").parent().addClass("menu-item-has-children");
    $(".responsive-mobile-menu ul li.menu-item-has-children > a").on("click", function() {
      $(this).parent().toggleClass("active").siblings().removeClass("active");
      $(this).next("ul").slideToggle();
      $(this).parent().siblings().find("ul").slideUp();
      return false;
    });
    $("html, .menu-btn.active").on("click", function() {
      $(".responsive-mobile-menu").removeClass("active");
      $(".menu-btn").removeClass("active");
    });
    $(".menu-btn, .responsive-mobile-menu").on("click", function(e) {
      e.stopPropagation();
    });
  }

  //  ============= ACCORDION TOGGLE TABS ===============

  $(".page-loading").fadeOut();

  //  ============= ACCORDION TOGGLE TABS ===============

  if ($('.toggle').length) {
    $(".toggle").each(function(){
      $(this).find('.content').hide();
      $(this).find('h4:first').addClass('active').next().slideDown(500).parent().addClass("activate");
      $('h4', this).on("click touchstart", function() {
          if ($(this).next().is(':hidden')) {
            $(this).parent().parent().parent().find("h4").removeClass('active').next().slideUp(500).removeClass('animated fadeInUp').parent().removeClass("activate");
            $(this).toggleClass('active').next().slideDown(500).addClass('animated fadeInUp').parent().toggleClass("activate");
          }
      });
    });
  }

  //  ============= SEARCH BOX ===============

  if ($('.search-icon').length) {
    $(".search-icon").on("click", function() {
      $(".search-bar").slideToggle();
      return false;
    });
  }
 
  //  ============= CART ITEM COUNTER ===============

  if ($('.minus-btn').length) {
    $('.minus-btn').on('click', function(e) {
      e.preventDefault();
      var $this = $(this);
      var $input = $this.closest('div').find('input');
      var value = parseInt($input.val());
      if (value > 1) {
        value = value - 1;
      } else {
        value = 0;
      }
      $input.val(value);
    });
  }

  if ($('.plus-btn').length) {
    $('.plus-btn').on('click', function(e) {
      e.preventDefault();
      var $this = $(this);
      var $input = $this.closest('div').find('input');
      var value = parseInt($input.val());
      if (value < 100) {
        value = value + 1;
      } else {
        value =100;
      }
      $input.val(value);
    });
  };

  //  ============= CUSTOM TAB (CHECKOUT PAGE) ===============

  if ($('.oct-table-head ul').length) {
    $(".oct-table-head ul").on("click", function() {
      $(this).parent().parent().toggleClass("active");
      return false;
    })
  };

  //  ============= DEFAULT THEME BUTTON ANIMATION ===============
    
  if ($('.btn-default').length) {
    $('.btn-default').on('mouseenter', function(e) {
      var parentOffset = $(this).offset(),
      relX = e.pageX - parentOffset.left,
      relY = e.pageY - parentOffset.top;
      $(this).find('span').css({top:relY, left:relX})}).on('mouseout', function(e) {
      var parentOffset = $(this).offset(),
      relX = e.pageX - parentOffset.left,
      relY = e.pageY - parentOffset.top;
      $(this).find('span').css({top:relY, left:relX})
    });
  };

  // AJAX CONTACT FORM SCRIPT (WORKING CONTACT FORM)

  if($('#contact-form').length){
    $('#submit').on("click", function(){
      var o = new Object();
      var form = '#contact-form';
      var name = $('#contact-form .name').val();
      var email = $('#contact-form .email').val();
      if(name == '' || email == '') {
        $('#contact-form .response').html('<div class="failed">Please fill the required fields.</div>');
        return false;
      }
      $.ajax({
          url:"mail.php",
          method:"POST",
          data: $(form).serialize(),
          beforeSend:function(){
              $('#contact-form .response').html('<div class="text-info"><img src="assets/images/preloader.gif"> Loading...</div>');
          },
          success:function(data){
              $('form').trigger("reset");
              $('#contact-form .response').fadeIn().html(data);
              setTimeout(function(){
                  $('#contact-form .response').fadeOut("slow");
              }, 5000);
          },
          error:function(){
              $('#contact-form .response').fadeIn().html(data);
          }
      });
    });
  };

});
