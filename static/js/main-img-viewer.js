
$(".images img").click(function(){
  $("#full-image").attr("src", $(this).attr("src"));
  $('#image-viewer').show();
});

$(".close").click(function(){
  $('#image-viewer').hide();
});
