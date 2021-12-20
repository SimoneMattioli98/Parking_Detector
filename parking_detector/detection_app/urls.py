from django.urls import path
from .views import home_view_detection, use_service

urlpatterns = [
    path('', home_view_detection),
    path('use_service/', use_service)

]