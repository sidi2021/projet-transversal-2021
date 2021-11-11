var date = new Date()
try {
  document.getElementById("copyright").innerHTML += date.getFullYear()
  document.getElementById("sitetile").innerHTML += String(date.getFullYear() - 1) + "-" + String(date.getFullYear())
} catch (e) {

}
var menu = document.getElementById('menu');
var menuTop = document.getElementById('menu-top');
var menuCenter = document.getElementById('menu-center');
var menuBottom = document.getElementById('menu-bottom');
var nav = document.getElementsByTagName("nav")[0];
var dropped = false;
var loginViewChanged = false;
var registerViewChanged = false;


try {
  menu.addEventListener('click', (e) => {
    menuTop.style.transition = "transform 0.5s"
    menuBottom.style.transition = "transform 0.5s"
    nav.style.transition = "height 1s"
    if (!dropped) {
      menu.style.backgroundColor = "rgba(255, 255, 255, 0.1)"
      menuTop.style.transform = "rotate(-45deg) translate(-5px, 6px)"
      menuCenter.style.display = "none"
      menuBottom.style.transform = "rotate(45deg)"
      dropped = true
    } else {
      menu.style.backgroundColor = "initial"
      menuTop.style.transform = "initial"
      menuCenter.style.display = "block"
      menuBottom.style.transform = "initial"
      dropped = false
    }

  })

} catch (e) {

}

try {
  document.getElementById('accueil').addEventListener('click', (e) => {
    document.title = 'Accueil'
  })
} catch (e) {

}

try {
  document.getElementById('footer-accueil').addEventListener('click', (e) => {
    document.title = 'Accueil'
  })
} catch (e) {

}

if (document.title === '') document.title = 'Accueil'
var navLinks = document.getElementsByClassName('nav-link')



try {

  document.getElementById('inscrire').addEventListener('click', (e) => {
    document.getElementById('identifier').click();
    $('#register_email').focus();
  })
  document.getElementById('identifier').addEventListener('click', (e) => {
    document.getElementById('inscrire').click().
    $('#login_email').focus();
  })
} catch (e) {

}

try {
  function showPassword1(input1) {
    var x = document.getElementById(input1);
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }

  function showPassword2(input1, input2) {
    var x = document.getElementById(input1);
    var y = document.getElementById(input2);
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
    if (y.type === "password") {
      y.type = "text";
    } else {
      y.type = "password";
    }
  }

} catch (e) {

}


function validateForm(formID) {

  var formInvalid = true;
  $(formID).each(function() {
    if ($.trim($(this).val()).length == 0) {
      formInvalid = false;
    }
  });

  return formInvalid;
}



try {
  $('.js-pscroll').each(function(){
    var ps = new PerfectScrollbar(this);

    $(window).on('resize', function(){
      ps.update();
    })
  });

} catch (e) {

}
