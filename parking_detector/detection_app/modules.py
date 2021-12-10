import cv2
import csv
import json
def draw_boxes(img, mapping):
    x_ = img.shape[1]
    y_ = img.shape[0]
    x_scale = x_ / 2592
    y_scale = y_ / 1944 
    img_copy = img.copy()
    for slot in mapping: #we skip the 
        bbox = slot["bbox"]
        details = slot["details"]
        x = round(int(bbox["x"]) * x_scale)
        y = round(int(bbox["y"]) * y_scale)
        w = round(int(bbox["w"]) * x_scale )
        h = round(int(bbox["h"]) * y_scale)
        cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 0, 255), 2)

    return img_copy


#Temporary function for mapping from csv to json
def remap(csv_path):
    with open(csv_path, mode='r') as infile:
        reader = csv.reader(infile)
        parking = [{
                    "bbox": {
                        "x": rows[1], 
                        "y": rows[2], 
                        "w": rows[3], 
                        "h": rows[4]
                    },
                    "details":{
                        "parking_id": None,
                        "slot_id": rows[0],
                        "slot_type": "car"
                    }
                } for rows in reader]
        jsonString = json.dumps(parking)
        jsonFile = open("stall_mapping/camera8.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()