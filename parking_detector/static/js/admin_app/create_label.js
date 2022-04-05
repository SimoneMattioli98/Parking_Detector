url_acquisition = "http://172.17.84.11:7000/acquisition/"
url_admin = "http://172.17.84.11:7000/admin/"
const standard_btn_color = "#33ccff"
const clicked_btn_color = "#1791b9"
let prev_clicked = null


var image = new Image(); 
var paper = NaN
var currentModSlot = -1
var points = []
var slots = new Map();
var isSaved = true
var currentCameraId = -1
document.addEventListener("keydown", deleteLabel, false);

  
//When the user clicks on a camera this function will be triggered

function serviceRequest(id){
    if(!isSaved){
        alert("You must first save your changes!")
        return
    }
    //Change button color if clicked and restore the previous button clicked color
    if(prev_clicked != null && prev_clicked != id){
        document.getElementById(prev_clicked).style.background = standard_btn_color
    }
    prev_clicked = id
    currentCameraId = id
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
            if(res["image"] == null){
                alert("Error! The camera was not found..")
                image.src = ""
            }else{
                //Once the frame is received it is sent to the service
                res = JSON.parse(xmlHttp.response);

                image = new Image(); 

                currentModSlot = -1
                points = []
                slots = new Map();

                image.src = "data:image/jpeg;base64," + res["image"];

                image.onload = main; 
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
    if(paper){
        paper.clear()
        document.getElementById("raph").innerHTML = "";
    }

    paper = Raphael(document.getElementById("raph"), image.width, image.height);
    var img = paper.image(image.src, 0, 0, image.width, image.height);
    if(res["mapping"] != null){
        buildJson(res["mapping"])
    }
    img.click(function(){
        var clientX = window.event.clientX;
        var clientY = window.event.clientY;
        var svg = document.getElementsByTagName("image");
        var rect = svg[0].getBoundingClientRect();
        var x = clientX - rect.left
        var y = clientY - rect.top
        
        var point = paper.rect(x, y, 5, 5).attr({fill: "#000"});
        point.drag(onDragMove, onDragStart, onDragComplete);
        points.push(point)

        if(points.length == 4){
            let r = Math.floor((Math.random() * 255));
            let g = Math.floor((Math.random() * 255));
            let b = Math.floor((Math.random() * 255));
            var poly = paper.path("M"+points[0].getBBox().x+","+points[0].getBBox().y+
                               "L"+points[1].getBBox().x+","+points[1].getBBox().y+
                               "L"+points[2].getBBox().x+","+points[2].getBBox().y+
                               "L"+points[3].getBBox().x+","+points[3].getBBox().y+
                               "Z").attr({fill: "rgba("+r+","+g+","+b+", 0.8)"});
            
            const temp = new Map()

            const points_map = new Map()
            points_map.set(points[0].id, points[0])
            points_map.set(points[1].id, points[1])
            points_map.set(points[2].id, points[2])
            points_map.set(points[3].id, points[3])

            const info = new Map()
            info.set("parking_id", null)
            info.set("slot_id", null)
            info.set("slot_type", null) 

            temp.set("points", points_map)
            temp.set("info", info)

            slots.set(poly.id, temp)
            poly.click(changeModSlot)   
            isSaved = false
            points = []
        }
     });
}


function changeSlotID(input_id) {
    if(currentModSlot > 0){
        slots.get(currentModSlot).get("info").set("slot_id", input_id.value)
    }else{
        alert("No slot selected");
        input_id.value = ''
    }
}

function changeSlotType(input_type) {
    if(currentModSlot > 0){
        slots.get(currentModSlot).get("info").set("slot_type", input_type.value)
    }else{
        alert("No slot selected");
        input_type.value = ''
    }  
}

function deleteLabel(e) {
    var key = e.key;
    if(key=="Delete" && currentModSlot >= 0) {
        for (const value of slots.get(currentModSlot).get("points").values()) {
            value.remove()
        }
        paper.getById(currentModSlot).remove()
        slots.delete(currentModSlot)
        currentModSlot = -1
        isSaved = false
        document.getElementById("slot_id").value = '';
        document.getElementById("slot_type").value = '';
    }
}

function onDragStart(){
    if(currentModSlot >= 0 && slots.get(currentModSlot).get("points").has(this.id)){
        this.ox = this.attr('x');
        this.oy = this.attr('y');    
    }
}


function onDragMove(dx,dy){
    if(currentModSlot >= 0 && slots.get(currentModSlot).get("points").has(this.id)){
        this.attr({x: this.ox + dx, y: this.oy + dy });
    }
}

function onDragComplete(){
    if(currentModSlot >= 0 && slots.get(currentModSlot).get("points").has(this.id)){
        temp = []
        for (const value of slots.get(currentModSlot).get("points").values()) {
            temp.push([value.getBBox().x, value.getBBox().y])
        }
        var newPath =   ["M",temp[0][0],temp[0][1],
                         "L",temp[1][0],temp[1][1],
                         "L",temp[2][0],temp[2][1],
                         "L",temp[3][0],temp[3][1],
                         "Z"]

        paper.getById(currentModSlot).attr({ path : newPath });
    }
};


function changeModSlot(){
    if(currentModSlot >= 0){
        paper.getById(currentModSlot).attr({opacity: "0.8"})
    }
    currentModSlot = this.id
    for (const value of slots.get(currentModSlot).get("points").values()) {
        value.toFront()
    }
    paper.getById(currentModSlot).attr({opacity: "0.4"})

    var slot_id_input = document.getElementById("slot_id");
    var slot_type_input = document.getElementById("slot_type");
    var slot_id = slots.get(currentModSlot).get("info").get("slot_id")
    var slot_type = slots.get(currentModSlot).get("info").get("slot_type")

    if(slot_id == null){
        slot_id_input.value = ""
    }else{
        slot_id_input.value = slot_id
    }

    if(slot_type == null){
        slot_type_input.value = ""
    }else{
        slot_type_input.value = slot_type
    }


}
function buildJson(){
    var mapping = JSON.parse(res["mapping"])
    for(const slot of mapping){

        points = []
        console.log(slot)
        for(const point_json of slot["points"]){
            var point = paper.rect(point_json[0], point_json[1], 5, 5).attr({fill: "#000"});
            point.drag(onDragMove, onDragStart, onDragComplete);
            points.push(point)
        }

        let r = Math.floor((Math.random() * 255));
        let g = Math.floor((Math.random() * 255));
        let b = Math.floor((Math.random() * 255));
        var poly = paper.path("M"+points[0].getBBox().x+","+points[0].getBBox().y+
                            "L"+points[1].getBBox().x+","+points[1].getBBox().y+
                            "L"+points[2].getBBox().x+","+points[2].getBBox().y+
                            "L"+points[3].getBBox().x+","+points[3].getBBox().y+
                            "Z").attr({fill: "rgba("+r+","+g+","+b+", 0.8)"});
        
        const temp = new Map()

        const points_map = new Map()
        points_map.set(points[0].id, points[0])
        points_map.set(points[1].id, points[1])
        points_map.set(points[2].id, points[2])
        points_map.set(points[3].id, points[3])

        const info = new Map()
        info.set("parking_id", slot["details"]["parking_id"])
        info.set("slot_id", slot["details"]["slot_id"])
        info.set("slot_type", slot["details"]["slot_type"]) 

        temp.set("points", points_map)
        temp.set("info", info)

        slots.set(poly.id, temp)
        poly.click(changeModSlot)
        points = []   
        
    }
}


 
function saveJson(){
    var json_array = []
    var check_correctness = true
    if(slots.size > 0){
        
        for (const slot of slots.values()) {
            var json_dict = {'points': [], 'details': {}}
            for(const point of slot.get("points").values()){
                var bbox = point.getBBox()
                json_dict["points"].push([bbox.x, bbox.y])
            }
            
            json_dict['details']['parking_id'] = slot.get("info").get("parking_id")
            var slot_id = slot.get("info").get("slot_id") 
            var slot_type = slot.get("info").get("slot_type")
            if(slot_id == null || slot_type == null){
                check_correctness = false
            }
            json_dict['details']['slot_id'] = slot_id
            json_dict['details']['slot_type'] = slot_type  
            
            json_array.push(json_dict)
        }

        if(check_correctness){
            json_file = JSON.stringify(json_array)
            isSaved = true
            console.log(json_file)
            csrftoken = getCookie('csrftoken'); 
            var xmlHttp = new XMLHttpRequest();
    
            xmlHttp.open("POST", url_admin, true); // true for asynchronous 
            xmlHttp.setRequestHeader("X-CSRFToken", csrftoken); 
            xmlHttp.send(JSON.stringify({"id": currentCameraId,"mapping": json_file}));
        }else{
            alert("Not all slots have been completed.")
        }
        
        
    }
}
