from django.shortcuts import render
from django.http.response import HttpResponse
from .modules import draw_boxes
import base64
import cv2
from io import BytesIO
from PIL import Image
import numpy as np
# Create your views here.

# the user wants to get the parking slots availlable 
def acquire_detections(request):

    if request.method == 'GET':
        return render(request, "detection_app/acquire_detections.html")

# this is the API which shows the results of the detections
def use_service(request):
    if request.method == 'GET': 
        return render(request, "detection_app/show_results.html")

    if request.method == "POST":
        print(type(request.body))
        dataBytesIO = BytesIO(request.body)        
        pil_img = Image.open(dataBytesIO)
        opencv_img = np.array(pil_img) 
        opencv_img = opencv_img[:, :, ::-1].copy() 
        img = draw_boxes(opencv_img, 'stall_mapping/camera8.csv')
        cv2.imshow("Image", img)
        cv2.waitKey()
        cv2.destroyAllWindows()
        return HttpResponse("LOL")