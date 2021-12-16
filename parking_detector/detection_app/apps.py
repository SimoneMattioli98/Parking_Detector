from django.apps import AppConfig
from model.yolo import YoloModel
import yaml

class DetectionAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'detection_app'

    with open("configuration/detection_config.yaml", "r") as yamlfile:
        configuration = yaml.load(yamlfile, Loader=yaml.FullLoader)

    VERSION = configuration["yolo"]["version"] 
    FOLDER = configuration["yolo"]["folder"]
    detector = YoloModel(VERSION, FOLDER)
    detector.build_model()
