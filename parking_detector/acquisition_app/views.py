from django.http.response import HttpResponse
from django.shortcuts import render
import json
import base64
# Create your views here.

def acquire_image(request):

    camera_id = (request.body).decode("utf-8") 

    camera_data = {"image": None, "mapping": None}

    try:
        with open(f"media/camera{camera_id}.jpg", "rb") as f:
            image_bytes = f.read()
            image_b64 = base64.b64encode(image_bytes) #we first create a string 
            image_ascii = image_b64.decode('ascii')  #we decode it to ascii characters
            camera_data['image'] = image_ascii #we use the ascii image inside the json because it is serializable

            mapping = open(f"stall_mapping/camera{camera_id}.json", "r")
            mapping_content = mapping.read()
            camera_data["mapping"] = mapping_content
            
    except IOError:
        pass
        
    return HttpResponse(json.dumps(camera_data))