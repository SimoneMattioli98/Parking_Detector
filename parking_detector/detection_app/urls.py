from django.urls import path
from .views import acquire_detections, use_service

urlpatterns = [
    path('', acquire_detections),
    path('use_service/', use_service)

]