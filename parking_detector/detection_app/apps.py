from django.apps import AppConfig
from model.yolo import YoloModel

class DetectionAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'detection_app'
    VERSION = 'yolov5s'  # or yolov5m, yolov5l, yolov5x, custom
    FOLDER = "ultralytics/yolov5"
    detector = YoloModel(VERSION, FOLDER)
    detector.build_model()
