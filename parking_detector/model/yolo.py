import torch 
import numpy as np


class YoloModel:
    def __init__(self, version, folder) -> None:
        self.version = version
        self.model = None
        self.folder = folder
        #classes which wants to be detected
        self.CLASSES_TO_DETECT = {
            2 : 'car',
            5 : 'bus',
            7 : 'truck',
        }


    def build_model(self):
        # CHANGE MODEL TYPE BASED ON VERSION AND SIZE
        self.model = torch.hub.load(self.folder, self.version)
        print("Model Built!")

    def get_detection(self, image):
        if self.model == None:
            print("First you need to build the model")
        else:
            #coordinates a retriven as x1,y1,x2,y2
            results = self.model(image).xyxy[0]
            mask = np.isin(results[:,5],list(self.CLASSES_TO_DETECT.keys()))
            detections = results[mask]
            return detections