  var clicked = false
  $(document).ready(function() {
    $("#settings-btn").on("click", function(e) {

      var x = $("#settings-btn").offset().left;
      var el = $("#settings-popup");
      if (!clicked) {
        el.css('position', 'absolute');
        el.css('display', 'inherit');
        el.css("left", x - 111);
        el.css("top", 63);
        clicked = true
      } else {
        el.css('display', 'none');
        clicked = false
      }
    })
    $(document).mouseup(function(e) {
      var container = $("#settings-popup");
      if (!container.is(e.target) && container.has(e.target).length === 0) {
        $("#settings-popup").css('display', 'none');
      }
    });
    $(window).resize(function() {
      $("#settings-popup").css('display', 'none');
    });



  })



try {
  document.getElementById('image-change').addEventListener('click', (e) => {
    document.getElementById('file_input').click()
    e.setAttribute('src', document.getElementById('file_input').files[0])
  })
} catch (e) {

}


try {
  Array.prototype.forEach.call(document.querySelector('.hide-alert'), function (el){
    setTimeout(function() {
        el.style.display = 'none'
    }, 3000);
  })

} catch (e) {}
