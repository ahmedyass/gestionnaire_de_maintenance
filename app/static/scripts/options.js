var local = document.getElementById('localisation');
var res = document.getElementById('ressource');
var res_id = parseInt(window.location.pathname.split("/")[1])
local.onchange = function() {
    var loocali = local.value;
    fetch('/ressources/'+loocali).then(function(response) {
        response.json().then(function(data) {
            var optionHTML = '';
            for (var ressource of data.ressources) {
                if (ressource.id == res_id) {
                    optionHTML += '<option value="' + ressource.id +'" selected>' + ressource.nom + '</option>';
                }
                else {
                    optionHTML += '<option value="' + ressource.id +'">' + ressource.nom + '</option>';
                }
            }
            res.innerHTML = optionHTML;
        });
    });
    
}