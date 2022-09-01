/** Code By Webdevtrick ( https://webdevtrick.com )  **/
$('input').on('focusin', function() {
    $(this).parent().find('.labelanimation').addClass('active');
  });

  $('input').on('focusout', function() {
    if (!this.value) {
      $(this).parent().find('.labelanimation').removeClass('active');
    }
  });
