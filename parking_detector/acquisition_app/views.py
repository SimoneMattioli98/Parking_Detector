from django.http.response import HttpResponse
from django.shortcuts import render
import json
import base64
import parking_detector.utility_function as utils
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def acquire_image(request):

    camera_id = (request.body).decode("utf-8") 

    camera_data = {"image": None, "mapping": None}

    try:
        with open(f"media/camera{camera_id}.jpg", "rb") as f:
            image_bytes = f.read()
            camera_data['image'] = utils.send_image_process(image_bytes) 

            mapping = open(f"labels/camera{camera_id}.json", "r")
            mapping_content = mapping.read()
            camera_data["mapping"] = mapping_content
            
    except IOError:
        pass
        
    return HttpResponse(json.dumps(camera_data))