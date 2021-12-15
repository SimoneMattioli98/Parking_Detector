from django.apps import AppConfig
from model.yolo import YoloModel

class DetectionAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'detection_app'
    VERSION = "v4"
    SIZE = "full"
    FOLDER = "model/building_files"
    detector = YoloModel(VERSION, SIZE, FOLDER)
    detector.build_model()
