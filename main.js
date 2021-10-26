if (window.addEventListener) {
    window.addEventListener('load', function () { init(); });
}
var enableDraw = false;
var started = false;
var canvas, context;
var stampId = '';
var lastColor = 'black';
var lastStampId = '';
var Maindata = ""
function init() {

    canvas = $('#imageView').get(0);
    context = canvas.getContext('2d');
    // Auto-adjust canvas size to fit window.
    canvas.width = window.innerWidth - 75;
    canvas.height = window.innerHeight - 75;
    canvas.addEventListener('mousedown', mousemove, false);
    canvas.addEventListener('mouseup', mouseUp, false);
    //$('#container').get(0).addEventListener('mousemove', onMouseMove, false);
    canvas.addEventListener('mousemove', onMouseMove, false);
    canvas.addEventListener('click', onClick, false);

    // Add events for toolbar buttons.
    $('#red').get(0).addEventListener('click', function (e) { onColorClick(e.target.id); }, false);
    $('#pink').get(0).addEventListener('click', function (e) { onColorClick(e.target.id); }, false);
    $('#fuchsia').get(0).addEventListener('click', function (e) { onColorClick(e.target.id); }, false);
    $('#orange').get(0).addEventListener('click', function (e) { onColorClick(e.target.id); }, false);
    $('#yellow').get(0).addEventListener('click', function (e) { onColorClick(e.target.id); }, false);
    $('#lime').get(0).addEventListener('click', function (e) { onColorClick(e.target.id); }, false);
    $('#green').get(0).addEventListener('click', function (e) { onColorClick(e.target.id); }, false);
    $('#blue').get(0).addEventListener('click', function (e) { onColorClick(e.target.id); }, false);
    $('#purple').get(0).addEventListener('click', function (e) { onColorClick(e.target.id); }, false);
    $('#black').get(0).addEventListener('click', function (e) { onColorClick(e.target.id); }, false);
    $('#white').get(0).addEventListener('click', function (e) { onColorClick(e.target.id); }, false);
    $('#fill').get(0).addEventListener('click', function (e) { onFill(); }, false);
    var firebaseConfig = {
        apiKey: "AIzaSyD-dljA9xatC5tY_xntrR1fMZZcv0H3qvM",
        authDomain: "hackilo-edutech-contact-form.firebaseapp.com",
        databaseURL: "https://hackilo-edutech-contact-form-default-rtdb.firebaseio.com",
        projectId: "hackilo-edutech-contact-form",
        storageBucket: "hackilo-edutech-contact-form.appspot.com",
        messagingSenderId: "590022236783",
        appId: "1:590022236783:web:75b6cbd0ebd67e23cccb9a",
        measurementId: "G-LSNMWPXBNK"
    };
    firebase.initializeApp(firebaseConfig);
    
     firebase.database().ref("Data").on('value', (snapshot) => {
        const data = snapshot.val()['base64']
        var image = new Image();
        image.onload = function () {
            context.drawImage(image, 0, 0);
        };
        image.src = data;
      
    
    })
}
function onMouseMove(ev) {
    var x, y;

    // Get the mouse position.
    if (ev.layerX >= 0) {
        // Firefox
        x = ev.layerX;
        y = ev.layerY - 5;
    }
    else if (ev.offsetX >= 0) {
        // Opera
        x = ev.offsetX;
        y = ev.offsetY - 5;
    }
    if (enableDraw) {
        if (!started) {
            started = true;

            context.beginPath();
            context.moveTo(x, y);
        }
        else {
            context.lineTo(x, y);
            context.stroke();
        }
    }
    $('#stats').text(x + ', ' + y);
}

function onClick(e) {
    if (stampId.length > 0) {
        context.drawImage($(stampId).get(0), e.pageX - 90, e.pageY - 60, 80, 80);
    }
   
}

function onColorClick(color) {
    // Start a new path to begin drawing in a new color.
    context.closePath();
    context.beginPath();

    // Select the new color.
    context.strokeStyle = color;

    // Highlight selected color.
    var borderColor = 'white';
    if (color == 'white' || color == 'yellow') {
        borderColor = 'black';
    }

    $('#' + lastColor).css("border", "0px dashed white");
    $('#' + color).css("border", "1px dashed " + borderColor);

    // Store color so we can un-highlight it next time around.
    lastColor = color;
    var img = canvas.toDataURL("image/png");
    firebase.database().ref("Data").set({
        base64: img
    })

}

function onFill() {
    // Start a new path to begin drawing in a new color.
    context.closePath();
    context.beginPath();

    context.fillStyle = context.strokeStyle;
    context.fillRect(0, 0, canvas.width, canvas.height);
}

function onStamp(id) {
    // Update the stamp image.
    stampId = '#' + id;
    if (lastStampId == stampId) {
        // User clicked the selected stamp again, so deselect it.
        stampId = '';
    }

    $(lastStampId).css("border", "0px dashed white");
    $(stampId).css("border", "1px dashed black");

    // Store stamp so we can un-highlight it next time around.
    lastStampId = stampId;
}

function onSave() {
    var img = canvas.toDataURL("image/png");
    //  var link = document.createElement("a");

    //  document.body.appendChild(link); // for Firefox

    //  link.setAttribute("href", img);
    //  link.setAttribute("download", "download.png");
    //  link.click();
    document.getElementById("canvas_base64data").value = img;
    return true;
}
function Save_Canvas() {
    var img = canvas.toDataURL("image/png");
    var link = document.createElement("a");

    document.body.appendChild(link); // for Firefox

    link.setAttribute("href", img);
    link.setAttribute("download", "download.png");
    link.click();
}
function mousemove(e) {
    enableDraw = true;
    var img = canvas.toDataURL("image/png");
    firebase.database().ref("Data").set({
        base64: img
    })
}
function sleep(delay) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay);
}
function clr_canvas() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    // var img = canvas.toDataURL("image/png");
    firebase.database().ref("Data").set({
        base64: "data:image/png;base64,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"
    })
}
function mouseUp(e) { 
    enableDraw = false; 
    started = false;
    var img = canvas.toDataURL("image/png");
    firebase.database().ref("Data").set({
        base64: img
    })
}
