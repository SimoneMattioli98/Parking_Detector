from django.contrib import admin
from django.urls import path
from django.urls.conf import include, include
from .views import home_view

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('detection/', include('detection_app.urls')),
    path('acquisition/', include('acquisition_app.urls')),
    path("admin/", include('admin_app.urls')),
    path('', home_view)
]
