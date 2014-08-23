var score = 0;
var vidas = 4;

$(function() {
    if(getCookie('score') != '') {
        score = getCookie('score');
        vidas = getCookie('vidas');
    }

    var intVidas = parseInt(vidas);
    if(intVidas != 4) {
        for(var i = intVidas + 1; i <= 4; i++) {
            $('#vida' + i).css('visibility', 'hidden');
        }
    }

    $('#pontos').html(score);
    var count = 5;
    $('#maisdicas').click(function() {
        if(count <= 7) {
            $('#dica' + count).css('visibility','visible');
            count++;
        }
        return false;
    });

    $('#pular').click(function() {
        if(vidas != 1) {
            var intVidas = parseInt(vidas);
            intVidas--;
            $('#vida' + vidas).css('visibility', 'hidden');
            vidas = intVidas;
            setCookie('vidas',intVidas,1);
            window.location.reload();
        } else {
            window.location.href = "/hof";
        }
    });

    $('#enviar').click(function() {
        if($('#name').val() == $('#resposta').html()) {
            var intScore = parseInt(score)
            intScore += 100;
            setCookie('score',intScore,1);
            setCookie('vidas',vidas,1);
            location.reload();
        } else {
            if(vidas != 1) {
                var intVidas = parseInt(vidas);
                intVidas--;
                $('#vida' + vidas).css('visibility', 'hidden');
                vidas = intVidas;
                setCookie('vidas',intVidas,1);
            } else {
                window.location.href = "/hof";
            }
        }
    });
});

function setCookie(cname,cvalue,exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname+"="+cvalue+"; "+expires;
}
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) != -1) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}