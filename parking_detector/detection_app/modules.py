import cv2
import csv
import json
import numpy as np
from .apps import DetectionAppConfig



def get_stalls_mask(image,stalls) :
  #mask type define the maximum value of stall IDs supported
  mask_stalls = np.zeros(image.shape[:2] + (1,), dtype=np.uint16)
  for stall in stalls:

      points = np.expand_dims(np.array(stall["points"], dtype=np.int32), axis=0)
      stallo_id = int(stall['details']['slot_id'])
      
      #drawing poly on mask using its value id as color
      cv2.fillPoly(mask_stalls, points, stallo_id)
  return mask_stalls

def get_detection_masks(image, detections, classes) :
    x1,y1,x2,y2 = 0,1,2,3

    # mask used to detect busy stalls
    mask_detections = np.zeros(image.shape[:2] + (1,), dtype=np.uint8)

    # mask type define the maximum value of class IDs supported
    # mask used to retrieve what class is on a given stall
    mask_classes= np.zeros(image.shape[:2] + (1,), dtype=np.uint8)

    # drawing detections bounding boxes (only rectangular supported)
    for detection in zip(detections, classes) :
        bbox = detection[0]
        clas = detection[1]
        pnt1 = (int(bbox[x1]), int(bbox[y1]))
        pnt2 = (int(bbox[x2]), int(bbox[y2]))
        
        cv2.rectangle(mask_detections, pnt1, pnt2, 1, -1)
        cv2.rectangle(mask_classes, pnt1, pnt2, int(clas), -1)

    return mask_detections, mask_classes

def get_busy_stalls(mask_stalls, mask_detections, mark_veichles, stalls_size, classes_to_detect, mask_classes, threshold=0.6):
    # number of pixels per stall overlayed between stall and detections
    mask_overlay = mask_stalls * mask_detections
    unique, counts = np.unique(mask_overlay, return_counts=True)
    overlay_pixel = dict(zip(unique, counts))

    # dictionary stall_id -> detection_class
    busy_stalls = {}

    for stall, size in stalls_size.items():
        # discard background
        iou = 0
        if stall > 0:
            iou = overlay_pixel.get(stall, 0) / size
            print(iou)

        # if iou is greater that threshold, stall is marked as busy
        if iou >= threshold :
            cls,cnt = np.unique(np.where(np.isin(mask_stalls,stall),mask_classes,0),return_counts=True)

            # discard background
            m = np.isin(cls,0,invert=True)
            cls,cnt = cls[m], cnt[m]
            busy_stalls[stall] = classes_to_detect[cls[cnt.argmax()]]
    return busy_stalls
    

def draw_parking(image,stalls,detections) :

    stall_colors = DetectionAppConfig.configuration["stall_colors"]
    
    stalls_mask = image.copy()
    busy_stalls = list(detections.keys())
    
    for stall in stalls:
        #drawing stall with different color based on its state
        points = np.expand_dims(np.array(stall["points"], dtype=np.int32), axis=0)
        stall_id = int(stall['details']['slot_id'])
        cv2.fillPoly(stalls_mask, points, stall_colors['busy'] if np.isin(stall_id,busy_stalls) else stall_colors['free'])

        # to edit, label non properly shown
        text_wh = cv2.getTextSize(str(stall_id), cv2.FONT_HERSHEY_PLAIN, 1., 1)
        center_poly = np.mean(points[0], axis=0).astype(np.int32)
        cv2.putText(stalls_mask, str(stall_id), (center_poly[0] - text_wh[0][0], center_poly[1] + text_wh[0][1]), cv2.FONT_HERSHEY_PLAIN, 1., [0,0,0], 1)

    overlay = cv2.addWeighted(image.copy(), 0.5, stalls_mask, 0.5, 0)
    return overlay





#Temporary function for mapping from csv to json
def remap():
    id,x,y,w,h = 0,1,2,3,4

    fnc = lambda a,b=0 : round((int(a)+int(b))*scale)

    #to move
    scale=0.385
    with open("stall_mapping/camera2.csv", mode='r') as infile:
        reader = csv.reader(infile)

        parking = [{
            "points": [
                [fnc(rows[x]),fnc(rows[y])], 
                [fnc(rows[x]),fnc(rows[y],rows[h])], 
                [fnc(rows[x],rows[w]),fnc(rows[y],rows[h])], 
                [fnc(rows[x],rows[w]),fnc(rows[y])]
                ],
            "details":{
                "parking_id": None,
                "slot_id": rows[id],
                "slot_type": "car"
            }
        } for rows in reader]
        jsonString = json.dumps(parking)
        jsonFile = open("stall_mapping/camera2.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()