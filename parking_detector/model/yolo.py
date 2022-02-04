import torch
import numpy as np
import os

from yolox.exp import get_exp
from .predictor import Predictor
from yolox.data.datasets import COCO_CLASSES


class YoloModel:
    def __init__(self, checkpoint, tsize, device='gpu', confidence=0.2, nms=0.45, fp16=False, legacy=False) -> None:
        self.checkpoint = checkpoint
        self.conf = confidence
        self.nms = nms
        self.tsize = tsize
        self.device = device
        self.predictor = None
        self.fp16 = fp16
        self.legacy = legacy

    def __create_predictor__(self, exp):

        exp.test_conf = self.conf
        exp.nmsthre = self.nms
        exp.test_size = (self.tsize, self.tsize)

        model = exp.get_model()

        if self.device == "gpu":
            model.cuda()
            if self.fp16:
                model.half()  # to FP16
        model.eval()

        ckpt = torch.load(self.checkpoint, map_location="cpu")
        # load the model state dict
        model.load_state_dict(ckpt["model"])

        predictor = Predictor(
            model, exp, COCO_CLASSES, None, None,
            self.device, self.fp16, self.legacy,
        )

        return predictor

    def build_model(self):
        exp = get_exp(None, "yolox-s")
        self.predictor = self.__create_predictor__(exp)
        # CHANGE MODEL TYPE BASED ON VERSION AND SIZE
        print("Model Built!")

    def __predict__(self, image):
        outputs, img_info = self.predictor.inference(image)
        # result_image = self.predictor.visual(outputs[0], img_info, self.predictor.confthre)
        # cv2_imshow(result_image)
        return outputs[0], img_info

    def get_detection(self, image):
        if self.predictor is None:
            print("First you need to build the model")
        else:
            outputs, img_info = self.__predict__(image)

            ratio = img_info["ratio"]
            img = img_info["raw_img"]
            if outputs is None:
                return img
            output = outputs[0].cpu()

            # preprocessing: resize
            output[:, 0:4] /= ratio

            return output
