//When the user clicks on a camera this function will be triggered
document.getElementById("cam1").onclick =function () {
    url_detection = "http://127.0.0.1:8000/detection/use_service/"
    url_acquisition = "http://127.0.0.1:8000/acquisition/"
    getImage(url_detection, url_acquisition)
}

//Get the cookie for django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//Send the requesto to the acquisition module
function getImage(url_detection, url_acquisition)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
            //Once the frame is received it is sent to the service
            console.log(xmlHttp.response)
            sendImage(url_detection, xmlHttp.response);
        }
    }
    xmlHttp.open("GET", url_acquisition, true); // true for asynchronous 
    xmlHttp.responseType = 'arraybuffer';
    xmlHttp.send("CAM1");
}

//Send the image received from the acquisition to the service
function sendImage(url_detection, encoded_image)
{
    csrftoken = getCookie('csrftoken'); 
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", url_detection, true); // true for asynchronous 
    xmlHttp.setRequestHeader("X-CSRFToken", csrftoken); 
    xmlHttp.send(encoded_image);
}

