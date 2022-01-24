import torch 
import numpy as np
import os 

from yolox.exp import get_exp
from .predictor import Predictor
from yolox.data.datasets import COCO_CLASSES

class YoloModel:
    def __init__(self, version, folder) -> None:
        self.version = version
        self.predictor = None
        self.folder = folder
        #classes which wants to be detected
        self.CLASSES_TO_DETECT = {
            2 : 'car',
            5 : 'bus',
            7 : 'truck',
        }


    def __create_predictor__(self, exp):
        conf = 0.2
        nms = 0.45
        tsize = 1280
        device = "gpu"
        fp16 = False
        ckpt = "model/yolox_s.pth"
        legacy = False
    
        exp.test_conf = conf
        exp.nmsthre = nms
        exp.test_size = (tsize, tsize)

        model = exp.get_model()

        if device == "gpu":
            model.cuda()
            if fp16:
                model.half()  # to FP16
        model.eval()

        ckpt_file = ckpt
        ckpt = torch.load(ckpt_file, map_location="cpu")
        # load the model state dict
        model.load_state_dict(ckpt["model"])

        

        predictor = Predictor(
            model, exp, COCO_CLASSES, None, None,
            device, fp16, legacy,
        )
    
        return predictor 


    def build_model(self):
        exp = get_exp(None, "yolox-s")
        self.predictor = self.__create_predictor__(exp)
        # CHANGE MODEL TYPE BASED ON VERSION AND SIZE
        print("Model Built!")

    def __predict__(self, image):
        outputs, img_info = self.predictor.inference(image)
        result_image = self.predictor.visual(outputs[0], img_info, self.predictor.confthre)
        #cv2_imshow(result_image)
        return outputs, result_image, img_info

    def get_detection(self, image):
        if self.predictor == None:
            print("First you need to build the model")
        else:
            outputs, result_image, img_info = self.__predict__(image)
            #mask = np.isin(outputs[:,6],list(self.CLASSES_TO_DETECT.keys()))
            #detections = outputs[mask]
            return outputs
