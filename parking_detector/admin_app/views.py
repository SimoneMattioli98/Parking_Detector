from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json
# Create your views here.
@csrf_exempt
def label_view(request):
    if request.method == 'GET':
        return render(request, "admin_app/label_camera.html")
    if request.method == 'POST':
        response_json = json.loads(request.body.decode('utf8'))
        camera_id = response_json["id"]
        mapping = json.loads(response_json["mapping"])
        with open(f'labels/camera{camera_id}.json', 'w') as f:
            json.dump(mapping, f)
    
    return HttpResponse(status=200)