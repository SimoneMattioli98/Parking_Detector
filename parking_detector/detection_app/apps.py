from django.apps import AppConfig
from model.yolo import YoloModel
import yaml

class DetectionAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'detection_app'

    with open("configuration/detection_config.yaml", "r") as yamlfile:
        configuration = yaml.load(yamlfile, Loader=yaml.FullLoader)

    conf_yolo = configuration["yolo"]
    detector = YoloModel(conf_yolo["checkpoint"], conf_yolo["tsize"])
    detector.build_model()
