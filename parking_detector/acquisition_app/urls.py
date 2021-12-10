from django.urls import path
from .views import acquire_image
urlpatterns = [
    path('', acquire_image),
]