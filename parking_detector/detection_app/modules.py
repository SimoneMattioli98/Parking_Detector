import cv2
import csv

def draw_boxes(img, csv_path):
    with open(csv_path, mode='r') as infile:
            reader = csv.reader(infile)
            parking = {rows[0]: {"x": rows[1], "y": rows[2], "w": rows[3], "h": rows[4]} for rows in reader}
    
    x_ = img.shape[1]
    y_ = img.shape[0]
    x_scale = x_ / 2592
    y_scale = y_ / 1944 
    img_copy = img.copy()
    for id, slot in parking.items():
        if not id.isnumeric():
            continue
        x = round(int(slot["x"]) * x_scale)
        y = round(int(slot["y"]) * y_scale)
        w = round(int(slot["w"]) * x_scale )
        h = round(int(slot["h"]) * y_scale)
        cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 0, 255), 2)

    return img_copy