from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def label_view(request):
    if request.method == 'GET':
        return render(request, "detection_app/home_view_detection.html")
