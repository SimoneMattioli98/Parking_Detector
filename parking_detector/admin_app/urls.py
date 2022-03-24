from django.urls import path
from .views import label_view
urlpatterns = [
    path('', label_view),
]