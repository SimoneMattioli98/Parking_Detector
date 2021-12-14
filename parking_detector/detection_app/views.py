from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponseRedirect
from .modules import draw_boxes
import base64
import cv2
from io import BytesIO
from PIL import Image
import numpy as np
import json
from django.contrib import messages
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

        #IMAGE
        #we backwards repeat the operations we didf at sending time
        image_ascii = response_json["image"] 
        image_b64 = image_ascii.encode('ascii')
        image_bytes = base64.b64decode(image_b64)

        #MAPPING
        mapping = response_json["mapping"]
        mapping_json = json.loads(mapping)

        #process the image to numpy (opencv) so we can use it for detection
        imageBytesIO = BytesIO(image_bytes)
        pil_img = Image.open(imageBytesIO)
        opencv_img = np.array(pil_img) 
        opencv_img = opencv_img[:, :, ::-1].copy() #convert from RGB to BGR

        img = draw_boxes(opencv_img, mapping_json)

        camera_data = {"image": image_ascii, "mapping": None}
       
        return HttpResponse(json.dumps(camera_data))

    