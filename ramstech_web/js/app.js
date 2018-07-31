


var URL = '../php/ajax.php'
//var URL='http://localhost:4444/' use this if the server is running locally (and on port 4000)

var CATEGORIES = ["MOODS",
    "STYLES & DANSES",
    "MUSIQUE POUR",
    "INSTRUMENTS",
    "INSTRUMENTS ETHNIQUES",
    "PAYS",
    "TEMPOS",
    "TEXTURES",
    "FORMATION",
    "CARACTERE",
    "CARACTERISTIQUES TECHNIQUES",
    "MOUVEMENTS & TEXTURES"]

var blacklist = ["Mouvements", "Light", "Light", "Light Drama", "version principale", "Positif", "vocal/chanson/langue", "loisir", "TV", "instrumental", "cinéma", "Passion", "version alternative", "introduction"];




$("input:file").change(function () {

    var file = this.files[0];
    window.nativeURL = (window.webkitURL || window.URL);
    $("#audio").attr("src", window.nativeURL.createObjectURL(file));
	var player = document.getElementById("player");
    player.style.display = 'inline';
    player.load();
    var formdata = new FormData($("form")[0]);
    formdata.append("seuil_pred", 0.1);
    formdata.append("sort_by", "probability");
    $.ajax({

        url: URL,
        type: 'POST',
        data: formdata,
        cache: false,
        contentType: false,
        processData: false,
        success: function (data, statut) {

            if (!data['success']) {
                error_handling(data['ERR_MESSAGE']);

            }

            else {
                var preds = data['predictions'];

                foo(preds, '#general', CATEGORIES);
                foo(preds, '#menu1', ['INSTRUMENTS']);
                foo(preds, '#menu2', ['MOODS']);
                foo(preds, '#menu3', ['STYLES & DANSES']);
                var other_list = remove_list_from_list(CATEGORIES, ['INSTRUMENTS', 'MOODS', 'STYLES & DANSES']);
                foo(preds, '#menu4', other_list);

                $('#main_row').fadeIn();
            }
        }
    });
});



function remove_list_from_list(main_list, to_remove_list) {
    var new_list = [];
    for (var i = 0; i < main_list.length; i++) {
        if (!(to_remove_list.includes(main_list[i]))) {
            new_list.push(main_list[i]);
        }
    }
    return new_list;
}

function foo(preds, id, list_cats) {
    var list = get_top_n_for_cat(preds, 10, list_cats);
    if (list.length == 0) {
        text = "<p>Désolé, aucune indexation a été trouvée. Veuilez essayer avec un autre fichier.</p>"
    }
    else {

        var text = "<div class ='row'><div class='col-1'><ul>";
        for (var k in list) {
            text += '<li>' + list[k]['indexation']+'<span class ="indexation_titre">' + progressbar_from_val(list[k]['probability']) + '</span></li>';
        }
        text += "</ul></div></div>"
    }
    $(id).html(text);
}



function get_top_n_for_cat(preds, n, list_cats) {
    var top = [];
    for (var k in preds) {
        if (list_cats.includes(k)) {
            if (CATEGORIES.includes(k)) {
                for (var i in preds[k]) {
                    var indexation = preds[k][i];
                    if (!blacklist.includes(indexation['indexation'])) {
                        var split = indexation['indexation'].split('/');
                        indexation['indexation'] = split[split.length - 1];
                        top.push(preds[k][i]);
                    }
                }
            }
        }
    }
    return top.slice(0, n).sort(compare);
}


//OTHERS FUNCTIONS 

function compare(a, b) {
    if (a.probability > b.probability)
        return -1;
    if (a.probability < b.probability)
        return 1;
    return 0;
}


function progressbar_from_val(val) {
    var text = '<div class="progress" ><div class="progress-bar bg-success" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:' + val * 100 + '%">' + (val * 100).toFixed(1) + '</div></div>';
    return text;
}


function error_handling(error_text) {
    $('#error_block').fadeIn();

    switch (error_text) {
        case "ERR_TOO_SHORT_FILE":
            $('#error_message').html('Le fichier est trop court. Le fichier doit au moins faire 30 secondes.');
            break;
        case "ERR_TOO_LONG_FILE":
            $('#error_message').html('Le fichier est trop long. Le fichier doit faire au maximum 15 minutes.');
            break;
        case "ERR_INCORRECT_URL":
            $('#error_message').html("L'adresse fournie ne semble pas être correcte.");
            break;
        case "ERR_INCORRECT_ARGUMENT":
            $('#error_message').html("Il n'y a pas de fichier dans la requête.");
            break;
        case "ERR_INCORRECT_FILE_FORMAT":
            $('#error_message').html('Il semble que le fichier ne soit pas au format mp3.');
            break;
        default:
            $('#error_message').html('Erreur inconnue.');
    }

}


// SPINNER LOADING ICON

import {Spinner} from './spin.js';


var opts = {
  lines: 13, // The number of lines to draw
  length: 38, // The length of each line
  width: 17, // The line thickness
  radius: 45, // The radius of the inner circle
  scale: 0.5, // Scales overall size of the spinner
  corners: 1, // Corner roundness (0..1)
  color: '#000000', // CSS color or array of colors
  fadeColor: 'transparent', // CSS color or array of colors
  speed: 1, // Rounds per second
  rotate: 0, // The rotation offset
  animation: 'spinner-line-fade-quick', // The CSS animation name for the lines
  direction: 1, // 1: clockwise, -1: counterclockwise
  zIndex: 2e9, // The z-index (defaults to 2000000000)
  className: 'spinner', // The CSS class to assign to the spinner
  top: '50%', // Top position relative to parent
  left: '50%', // Left position relative to parent
  shadow: '0 0 1px transparent', // Box-shadow for the lines
  position: 'absolute' // Element positioning
};

var target = document.getElementById('load_zone');
var spinner = new Spinner(opts);

$(document).ajaxStart(function(){
    spinner.spin(target);

 }).ajaxStop(function(){
    spinner.stop();
});

$("#file_button").click(function (event) {
    $("#file_input").click();
    if ($('#error_block').is(':visible')) {
        $('#error_block').hide();
    }
});


// DRAG DROP

+ function($) {
    'use strict';


    var dropZone = document.getElementById('drop-zone');

    var startUpload = function(files) {
        console.log(files)
        var input = document.getElementById('file_input');
        input.files = files;
    }

    dropZone.ondrop = function(e) {
        e.preventDefault();
        this.className = 'upload-drop-zone';

        startUpload(e.dataTransfer.files)
    }

    dropZone.ondragover = function() {
        this.className = 'upload-drop-zone drop';
        return false;
    }

    dropZone.ondragleave = function() {
        this.className = 'upload-drop-zone';
        return false;
    }

}(jQuery);
