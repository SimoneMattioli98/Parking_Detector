from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponseNotFound
from .modules import draw_boxes
import base64
import cv2
from io import BytesIO
from PIL import Image
import numpy as np
import json
from django.contrib import messages
from utils import utils
# Create your views here.

# the user wants to get the parking slots availlable 
def acquire_detections(request):

    if request.method == 'GET':
        
        return render(request, "detection_app/acquire_detections.html")

# this is the API which shows the results of the detections
def use_service(request):
    # Shows the result of the prediction
    if request.method == "GET":
        return render(request, "detection_app/show_results.html")
    if request.method == "POST":
        response_json = json.loads((request.body).decode('utf8')) #we decode the message to be json

        if response_json["image"] == None or response_json["mapping"] == None:
            return HttpResponseNotFound("Error")
        #IMAGE
        #we backwards repeat the operations we didf at sending time
        image_string = response_json["image"] 
        image_acii = image_string.encode('ascii')
        image_bytes = base64.b64decode(image_acii)

        #MAPPING
        mapping = response_json["mapping"]
        mapping_json = json.loads(mapping)

        #process the image to numpy (opencv) so we can use it for detection
        imageBytesIO = BytesIO(image_bytes)
        pil_img = Image.open(imageBytesIO)
        opencv_img = np.array(pil_img) 

        #DETECTION PART
        preprocessed_img = draw_boxes(opencv_img, mapping_json)

        #In order to show the image we need it's byte version..
        bytes_image = utils.opencv_to_bytes(preprocessed_img)

        #..and it's serializable version
        sendable_image = utils.send_image_process(bytes_image)

        camera_data = {"image": sendable_image, "mapping": None}
       
        return HttpResponse(json.dumps(camera_data))

    