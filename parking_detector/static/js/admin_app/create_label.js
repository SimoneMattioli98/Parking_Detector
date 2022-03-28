url_acquisition = "http://172.17.84.11:7000/acquisition/"
const standard_btn_color = "#33ccff"
const clicked_btn_color = "#1791b9"
let prev_clicked = null

  
function saveJson(){
    var json_array = []
    var check_correctness = true
    if(slots.size > 0){
        
        for (const slot of slots.values()) {
            var json_dict = {"points": [], "details": {}}
            for(const point of slot.get("points").values()){
                var bbox = point.getBBox()
                json_dict["points"].push([bbox.x, bbox.y])
                console.log(json_dict["points"])
            }
            
            json_dict["details"]["parking_id"] = slot.get("info").get("parking_id")
            var slot_id = slot.get("info").get("slot_id") 
            var slot_type = slot.get("info").get("slot_type")
            if(slot_id == null || slot_type == null){
                check_correctness = false
            }
            json_dict["details"]["slot_id"] = slot_id
            json_dict["details"]["slot_type"] = slot_type  
            
            json_array.push(json_dict)
        }

        if(check_correctness){
            json_file = JSON.stringify(json_array)
            console.log(json_file)
        }else{
            alert("Not all slots have been completed.")
        }
        
        
    }
}



//When the user clicks on a camera this function will be triggered

function serviceRequest(id){
    //Change button color if clicked and restore the previous button clicked color
    if(prev_clicked != null && prev_clicked != id){
        document.getElementById(prev_clicked).style.background = standard_btn_color
    }
    prev_clicked = id
    document.getElementById(prev_clicked).style.background = clicked_btn_color

    getImage(url_acquisition, id)
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
function getImage(url_acquisition, id)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
            //Once the frame is received it is sent to the service
            res = JSON.parse(xmlHttp.response);
            if(res["image"] == null || res["mapping"] == null){
                alert("Error! The camera was not found..")
                image.src = ""
            }else{
                //Once the frame is received it is sent to the service
                res = JSON.parse(xmlHttp.response);
                const image = new Image(); 

                image.onload = main; 

                image.src = "data:image/jpeg;base64," + res["image"];
                console.log();
                free_slots.textContent = "Number of free slots: " + res["free_slots"];
            }
        }
    }
    xmlHttp.open("POST", url_acquisition, true); // true for asynchronous 
    //xmlHttp.responseType = 'arraybuffer';
    csrftoken = getCookie('csrftoken'); 
    xmlHttp.setRequestHeader("X-CSRFToken", csrftoken); 
    xmlHttp.send(id);
}


function main() {
    paper = Raphael(document.getElementById("raph"), image.width*0.8, image.height*0.8);
    var img = paper.image(image.src, 0, 0, image.width*0.8, image.height*0.8);
}
