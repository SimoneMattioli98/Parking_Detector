from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponseNotFound
from .modules import remap, get_stalls_mask, get_detection_masks, get_busy_stalls, draw_parking
import base64
import cv2
from io import BytesIO
from PIL import Image
import numpy as np
import json
from .apps import DetectionAppConfig
import parking_detector.utility_function as utility
from django.views.decorators.csrf import csrf_exempt


# the user wants to get the parking slots availlable 
@csrf_exempt
def home_view_detection(request):
    if request.method == 'GET':
        return render(request, "detection_app/home_view_detection.html")


# this is the API which shows the results of the detections
@csrf_exempt
def use_service(request):
    # Shows the result of the prediction
    if request.method == "GET":
        return render(request, "detection_app/show_results.html")
    if request.method == "POST":
        response_json = json.loads(request.body.decode('utf8'))  # we decode the message to be json

        if response_json["image"] is None or response_json["mapping"] is None:
            return HttpResponseNotFound("Error")
        # IMAGE
        # we backwards repeat the operations we didf at sending time
        image_string = response_json["image"]
        image_acii = image_string.encode('ascii')
        image_bytes = base64.b64decode(image_acii)

        # MAPPING
        mapping = response_json["mapping"]
        mapping_json = json.loads(mapping)

        # process the image to numpy (opencv) so we can use it for detection
        imageBytesIO = BytesIO(image_bytes)
        pil_img = Image.open(imageBytesIO)
        opencv_img = np.array(pil_img)
        print(opencv_img.shape)
        # DETECTION PART
        detections = DetectionAppConfig.detector.get_detection(opencv_img)
        mask_stalls = get_stalls_mask(opencv_img, mapping_json)
        unique, counts = np.unique(mask_stalls, return_counts=True)
        stalls_size = dict(zip(unique, counts))
        mask_detections = get_detection_masks(opencv_img, detections, DetectionAppConfig.configuration["classes_to_detect"])
        busy_stalls = get_busy_stalls(mask_stalls, mask_detections, stalls_size, threshold=0.6)

        preprocessed_img = draw_parking(opencv_img, mapping_json, busy_stalls)

        # In order to show the image we need it's byte version..
        bytes_image = utility.opencv_to_bytes(preprocessed_img)

        # ..and it's serializable version
        sendable_image = utility.send_image_process(bytes_image)

        camera_data = {"image": sendable_image, "free_slots": len(stalls_size) - len(busy_stalls) - 1}

        return HttpResponse(json.dumps(camera_data))
